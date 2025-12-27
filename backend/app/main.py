from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import os
from datetime import datetime
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
import io

app = FastAPI(
    title="Travel Photo Organizer API",
    description="Azure-based travel photo organization service",
    version="2.0.0"
)

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 환경 변수
ENVIRONMENT = os.getenv("ENVIRONMENT", "dev")
STORAGE_ACCOUNT_NAME = os.getenv("STORAGE_ACCOUNT_NAME", "")
AZURE_REGION = os.getenv("AZURE_REGION", "koreacentral")

# Pydantic Models
class HealthResponse(BaseModel):
    status: str
    environment: str
    timestamp: str
    storage_account: str
    region: str

class PhotoMetadata(BaseModel):
    id: str
    filename: str
    upload_date: str
    location: Optional[str] = None
    tags: List[str] = []

class Album(BaseModel):
    id: str
    name: str
    description: Optional[str] = None
    photo_count: int
    created_at: str


# EXIF 추출 함수
def get_decimal_from_dms(dms, ref):
    """DMS (도/분/초)를 십진법으로 변환"""
    try:
        degrees = float(dms[0])
        minutes = float(dms[1])
        seconds = float(dms[2])
        
        decimal = degrees + (minutes / 60.0) + (seconds / 3600.0)
        
        if ref in ['S', 'W']:
            decimal = -decimal
        
        return decimal
    except:
        return None

def extract_exif_data(image_bytes):
    """이미지에서 EXIF 데이터 추출"""
    try:
        image = Image.open(io.BytesIO(image_bytes))
        exif_data = image._getexif()
        
        if not exif_data:
            return None
        
        exif = {}
        gps_info = {}
        
        for tag_id, value in exif_data.items():
            tag = TAGS.get(tag_id, tag_id)
            
            if tag == "GPSInfo":
                for gps_tag_id, gps_value in value.items():
                    gps_tag = GPSTAGS.get(gps_tag_id, gps_tag_id)
                    gps_info[gps_tag] = gps_value
            else:
                exif[tag] = value
        
        result = {
            "datetime": exif.get("DateTime", None),
            "make": exif.get("Make", None),
            "model": exif.get("Model", None),
            "gps": None
        }
        
        # GPS 좌표 추출
        if gps_info.get("GPSLatitude") and gps_info.get("GPSLongitude"):
            lat = get_decimal_from_dms(
                gps_info["GPSLatitude"],
                gps_info.get("GPSLatitudeRef", "N")
            )
            lon = get_decimal_from_dms(
                gps_info["GPSLongitude"],
                gps_info.get("GPSLongitudeRef", "E")
            )
            
            if lat and lon:
                result["gps"] = {
                    "latitude": round(lat, 6),
                    "longitude": round(lon, 6)
                }
        
        return result
    
    except Exception as e:
        print(f"EXIF 추출 오류: {str(e)}")
        return None


# Routes
@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Welcome to Travel Photo Organizer API",
        "version": "2.0.0",
        "docs": "/docs"
    }

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    return HealthResponse(
        status="healthy",
        environment=ENVIRONMENT,
        timestamp=datetime.utcnow().isoformat(),
        storage_account=STORAGE_ACCOUNT_NAME,
        region=AZURE_REGION
    )

@app.get("/api/v1/photos", response_model=List[PhotoMetadata])
async def list_photos(skip: int = 0, limit: int = 100):
    """List all photos (mock data)"""
    mock_photos = [
        PhotoMetadata(
            id=f"photo_{i}",
            filename=f"paris_{i}.jpg",
            upload_date="2024-11-23T10:00:00Z",
            location="Paris, France",
            tags=["travel", "europe", "paris"]
        )
        for i in range(1, 6)
    ]
    return mock_photos[skip:skip + limit]

@app.post("/api/v1/photos/upload")
async def upload_photo(file: UploadFile = File(...)):
    """Upload a photo with EXIF extraction"""
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image")
    
    # 파일 읽기
    contents = await file.read()
    
    # EXIF 데이터 추출
    exif_data = extract_exif_data(contents)
    
    response = {
        "success": True,
        "message": "Photo uploaded successfully",
        "filename": file.filename,
        "size": len(contents),
        "content_type": file.content_type,
        "storage": "azure_blob_storage",
        "container": "uploads"
    }
    
    # EXIF 데이터가 있으면 추가
    if exif_data:
        response.update({
            "datetime": exif_data.get("datetime"),
            "gps": exif_data.get("gps"),
            "camera": f"{exif_data.get('make', '')} {exif_data.get('model', '')}".strip(),
            "location": None  # TODO: GPS → 주소 변환 (Geocoding)
        })
    else:
        response.update({
            "datetime": None,
            "gps": None,
            "camera": None,
            "location": None
        })
    
    return response

@app.get("/api/v1/albums", response_model=List[Album])
async def list_albums():
    """List all albums (mock data)"""
    mock_albums = [
        Album(
            id="album_1",
            name="Paris 2024",
            description="Trip to Paris",
            photo_count=15,
            created_at="2024-11-01T00:00:00Z"
        ),
        Album(
            id="album_2",
            name="Seoul 2024",
            description="Seoul city tour",
            photo_count=23,
            created_at="2024-10-15T00:00:00Z"
        )
    ]
    return mock_albums

@app.post("/api/v1/albums")
async def create_album(album: Album):
    """Create a new album (mock)"""
    return {
        "message": "Album created successfully",
        "album": album
    }

@app.get("/api/v1/albums/{album_id}")
async def get_album(album_id: str):
    """Get album details (mock)"""
    return Album(
        id=album_id,
        name="Sample Album",
        description="This is a sample album",
        photo_count=10,
        created_at="2024-11-23T00:00:00Z"
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)