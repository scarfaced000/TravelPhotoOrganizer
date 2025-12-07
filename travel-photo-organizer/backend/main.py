from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from exif_extractor import exif_extractor
from geocoder import geocoder
import os
from dotenv import load_dotenv
import uuid
from pathlib import Path

load_dotenv()

app = FastAPI(title="Travel Photo Organizer API")

UPLOAD_DIR = Path("./uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {
        "message": "Travel Photo Organizer API",
        "status": "running",
        "mode": "local"
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
        print(f"✅ File size: {len(contents)} bytes")
        
        # EXIF 추출
        exif_data = exif_extractor.extract_exif(contents)
        print(f"📊 EXIF data: {exif_data}")
        
        # GPS → 장소명 변환
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
        
        # 파일 저장
        file_id = str(uuid.uuid4())
        blob_name = f"{file_id}_{file.filename}"
        file_path = UPLOAD_DIR / blob_name
        
        with open(file_path, "wb") as f:
            f.write(contents)
        
        print(f"💾 Saved to: {file_path}")
        
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
        photos = []
        for file_path in UPLOAD_DIR.glob("*"):
            if file_path.is_file():
                photos.append({
                    "filename": file_path.name,
                    "path": str(file_path),
                    "size": file_path.stat().st_size
                })
        return {"count": len(photos), "photos": photos}
    except Exception as e:
        raise HTTPException(500, f"Failed to list photos: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
