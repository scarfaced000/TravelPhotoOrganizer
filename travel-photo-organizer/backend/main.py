from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from exif_extractor import exif_extractor
from geocoder import geocoder
from duplicate_detector import duplicate_detector
from album_organizer import album_organizer
import os
from dotenv import load_dotenv
import uuid
from pathlib import Path
import json

load_dotenv()

app = FastAPI(title="Travel Photo Organizer API")

UPLOAD_DIR = Path("./uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

METADATA_FILE = Path("./photo_metadata.json")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def load_metadata():
    if METADATA_FILE.exists():
        with open(METADATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def save_metadata(data):
    with open(METADATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

@app.get("/")
async def root():
    return {
        "message": "Travel Photo Organizer API",
        "status": "running",
        "mode": "local",
        "version": "2.0"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.post("/api/upload")
async def upload_photo(file: UploadFile = File(...)):
    print(f"📸 Received file: {file.filename}")
    
    if not file.content_type.startswith("image/"):
        raise HTTPException(400, "Only image files allowed")
    
    try:
        contents = await file.read()
        file_size = len(contents)
        print(f"✅ File size: {file_size} bytes")
        
        exif_data = exif_extractor.extract_exif(contents)
        print(f"📊 EXIF data: {exif_data}")
        
        location_info = None
        if exif_data.get("gps"):
            gps = exif_data["gps"]
            print(f"📍 GPS found: {gps}")
            
            if gps and "latitude" in gps and "longitude" in gps:
                print(f"🌍 Converting GPS to location...")
                location_info = geocoder.get_location_name(
                    gps["latitude"],
                    gps["longitude"]
                )
                print(f"🏙️ Location: {location_info}")
        else:
            print("❌ No GPS data in EXIF")
        
        file_id = str(uuid.uuid4())
        blob_name = f"{file_id}_{file.filename}"
        file_path = UPLOAD_DIR / blob_name
        
        with open(file_path, "wb") as f:
            f.write(contents)
        
        print(f"💾 Saved to: {file_path}")
        
        photo_metadata = {
            "file_id": file_id,
            "filename": file.filename,
            "storage_path": str(file_path),
            "size": file_size,
            "datetime": exif_data.get("datetime"),
            "camera": exif_data.get("camera"),
            "gps": exif_data.get("gps"),
            "location_name": location_info.get("location_name") if location_info else None,
            "location_address": location_info.get("display_name") if location_info else None,
        }
        
        metadata_list = load_metadata()
        metadata_list.append(photo_metadata)
        save_metadata(metadata_list)
        
        return {
            "success": True,
            "file_id": file_id,
            "filename": file.filename,
            "storage_location": f"local://{file_path}",
            "exif": exif_data,
            "location": location_info,
            "status": "uploaded"
        }
    
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(500, f"Upload failed: {str(e)}")

@app.get("/api/photos")
async def list_photos():
    try:
        metadata_list = load_metadata()
        return {
            "count": len(metadata_list),
            "photos": metadata_list
        }
    except Exception as e:
        raise HTTPException(500, f"Failed to list photos: {str(e)}")

@app.get("/api/duplicates")
async def find_duplicates():
    try:
        metadata_list = load_metadata()
        
        if not metadata_list:
            return {
                "message": "No photos uploaded yet",
                "duplicate_groups": []
            }
        
        duplicate_groups = duplicate_detector.find_duplicates(metadata_list)
        summary = duplicate_detector.get_duplicate_summary(duplicate_groups)
        
        return {
            "message": f"Found {len(duplicate_groups)} duplicate groups",
            "summary": summary,
            "duplicate_groups": duplicate_groups
        }
    
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(500, f"Failed to find duplicates: {str(e)}")

@app.post("/api/organize")
async def organize_photos():
    """사진 자동 정리: 장소별 + 중복 그룹별 앨범 생성"""
    try:
        metadata_list = load_metadata()
        
        if not metadata_list:
            raise HTTPException(400, "No photos to organize")
        
        # 1. 장소별 앨범 생성
        location_summary = album_organizer.organize_by_location(metadata_list)
        
        # 2. 중복 그룹 앨범 생성
        duplicate_groups = duplicate_detector.find_duplicates(metadata_list)
        duplicate_summary = album_organizer.organize_duplicates(duplicate_groups)
        
        return {
            "success": True,
            "message": "Photos organized successfully",
            "location_albums": location_summary,
            "duplicate_albums": duplicate_summary
        }
    
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(500, f"Failed to organize: {str(e)}")

@app.get("/api/albums")
async def get_albums():
    """앨범 구조 조회"""
    try:
        structure = album_organizer.get_album_structure()
        
        total_locations = len(structure["by_location"])
        total_duplicates = len(structure["duplicates"])
        
        return {
            "total_location_albums": total_locations,
            "total_duplicate_groups": total_duplicates,
            "structure": structure
        }
    
    except Exception as e:
        raise HTTPException(500, f"Failed to get albums: {str(e)}")

@app.delete("/api/photos/clear")
async def clear_all_photos():
    try:
        for file_path in UPLOAD_DIR.glob("*"):
            if file_path.is_file():
                file_path.unlink()
        
        save_metadata([])
        
        return {"message": "All photos cleared"}
    except Exception as e:
        raise HTTPException(500, f"Failed to clear photos: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
