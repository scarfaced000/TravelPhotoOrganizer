from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import os
from datetime import datetime

app = FastAPI(
    title="Travel Photo Organizer API",
    description="Azure-based travel photo organization service",
    version="1.0.0"
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


# Routes
@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Welcome to Travel Photo Organizer API",
        "version": "1.0.0",
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
    # TODO: Implement Azure Blob Storage integration
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
    """Upload a photo (mock)"""
    # TODO: Implement Azure Blob Storage upload
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image")
    
    return {
        "message": "Photo uploaded successfully",
        "filename": file.filename,
        "content_type": file.content_type,
        "storage": "azure_blob_storage",
        "container": "uploads"
    }

@app.get("/api/v1/albums", response_model=List[Album])
async def list_albums():
    """List all albums (mock data)"""
    # TODO: Implement database integration
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
    # TODO: Implement database integration
    return {
        "message": "Album created successfully",
        "album": album
    }

@app.get("/api/v1/albums/{album_id}")
async def get_album(album_id: str):
    """Get album details (mock)"""
    # TODO: Implement database integration
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
