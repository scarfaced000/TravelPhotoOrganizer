from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import os
from datetime import datetime
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
import io
from azure.storage.blob import BlobServiceClient
from azure.core.exceptions import ResourceNotFoundError
import uuid
from collections import defaultdict
from datetime import datetime, timedelta

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


#Blob Storage 연결 (Managed Identity 또는 Connection String)
STORAGE_ACCOUNT_KEY = os.getenv("STORAGE_ACCOUNT_KEY", "")
# Blob Service Client 초기화
if STORAGE_ACCOUNT_NAME and STORAGE_ACCOUNT_KEY:
    connection_string = f"DefaultEndpointsProtocol=https;AccountName={STORAGE_ACCOUNT_NAME};AccountKey={STORAGE_ACCOUNT_KEY};EndpointSuffix=core.windows.net"
    blob_service_client = BlobServiceClient.from_connection_string(connection_string)
else:
    blob_service_client = None
    print("⚠️ Warning: Storage Account credentials not configured")
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


def find_duplicate_groups(photos_metadata):
    """
    촬영 시간 기반으로 중복 사진 그룹 찾기
    - 10초 이내 연속 촬영된 사진들을 그룹으로 묶음
    """
    if not photos_metadata:
        return []
    
    # 촬영 시간 파싱 가능한 사진만 필터링
    valid_photos = []
    for photo in photos_metadata:
        if photo.get('datetime'):
            try:
                # EXIF datetime 형식: "2025:01:30 22:16:39"
                dt = datetime.strptime(photo['datetime'], "%Y:%m:%d %H:%M:%S")
                photo['parsed_datetime'] = dt
                valid_photos.append(photo)
            except:
                pass
    
    # 촬영 시간 순으로 정렬
    valid_photos.sort(key=lambda x: x['parsed_datetime'])
    
    # 그룹 생성
    groups = []
    current_group = []
    
    for i, photo in enumerate(valid_photos):
        if not current_group:
            current_group.append(photo)
        else:
            # 이전 사진과의 시간 차이
            time_diff = photo['parsed_datetime'] - current_group[-1]['parsed_datetime']
            
            # 10초 이내면 같은 그룹
            if time_diff.total_seconds() <= 10:
                current_group.append(photo)
            else:
                # 그룹이 2장 이상이면 중복으로 간주
                if len(current_group) >= 2:
                    groups.append(current_group)
                # 새 그룹 시작
                current_group = [photo]
    
    # 마지막 그룹 처리
    if len(current_group) >= 2:
        groups.append(current_group)
    
    return groups


def calculate_image_similarity(img1_bytes, img2_bytes):
    """
    간단한 이미지 유사도 계산 (파일 크기 기반)
    실제 환경에서는 perceptual hash 등 사용 권장
    """
    size1 = len(img1_bytes)
    size2 = len(img2_bytes)
    
    # 크기 차이 10% 이내면 유사
    size_diff = abs(size1 - size2) / max(size1, size2)
    
    return size_diff < 0.1  # 10% 이내

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
    """List all photos from Blob Storage"""
    
    if not blob_service_client:
        # Mock data (Blob Storage 미설정 시)
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
    
    try:
        # ✅ Blob Storage에서 실제 사진 목록 가져오기
        container_client = blob_service_client.get_container_client("uploads")
        blobs = list(container_client.list_blobs())
        
        photos = []
        for blob in blobs[skip:skip + limit]:
            photos.append(PhotoMetadata(
                id=blob.name.split('_')[0],  # UUID 부분
                filename=blob.name,
                upload_date=blob.last_modified.isoformat(),
                location=None,
                tags=[]
            ))
        
        return photos
        
    except Exception as e:
        raise HTTPException(500, f"Failed to list photos: {str(e)}")

@app.delete("/api/v1/photos/{photo_id}")
async def delete_photo(photo_id: str):
    """Delete a photo from Blob Storage"""
    
    if not blob_service_client:
        raise HTTPException(503, "Storage not configured")
    
    try:
        container_client = blob_service_client.get_container_client("uploads")
        
        # UUID로 시작하는 blob 찾기
        blobs = container_client.list_blobs(name_starts_with=photo_id)
        
        deleted = False
        for blob in blobs:
            blob_client = container_client.get_blob_client(blob.name)
            blob_client.delete_blob()
            deleted = True
            print(f"🗑️ Deleted: {blob.name}")
        
        if not deleted:
            raise HTTPException(404, "Photo not found")
        
        return {"message": "Photo deleted successfully", "id": photo_id}
        
    except ResourceNotFoundError:
        raise HTTPException(404, "Photo not found")
    except Exception as e:
        raise HTTPException(500, f"Failed to delete photo: {str(e)}")

@app.post("/api/v1/photos/upload")
async def upload_photo(file: UploadFile = File(...)):
    """Upload a photo with EXIF extraction and Blob Storage save"""
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image")
    
    # 파일 읽기
    contents = await file.read()
    
    # EXIF 데이터 추출
    exif_data = extract_exif_data(contents)
    
    # ✅ Blob Storage에 저장
    blob_url = None
    if blob_service_client:
        try:
            # 고유한 파일명 생성 (UUID + 원본 파일명)
            file_id = str(uuid.uuid4())
            blob_name = f"{file_id}_{file.filename}"
            
            # uploads 컨테이너에 업로드
            container_client = blob_service_client.get_container_client("uploads")
            blob_client = container_client.get_blob_client(blob_name)
            
            # 업로드
            blob_client.upload_blob(contents, overwrite=True)
            
            # Blob URL
            blob_url = blob_client.url
            
            print(f"✅ Uploaded to Blob Storage: {blob_name}")
            
        except Exception as e:
            print(f"❌ Blob Storage upload failed: {str(e)}")
            # 에러가 나도 API는 계속 진행 (EXIF 정보는 반환)
    
    response = {
        "success": True,
        "message": "Photo uploaded successfully",
        "filename": file.filename,
        "size": len(contents),
        "content_type": file.content_type,
        "blob_url": blob_url,  # ✅ Blob Storage URL 추가
        "storage": "azure_blob_storage" if blob_url else "memory_only"
    }
    
    # EXIF 데이터가 있으면 추가
    if exif_data:
        response.update({
            "datetime": exif_data.get("datetime"),
            "gps": exif_data.get("gps"),
            "camera": f"{exif_data.get('make', '')} {exif_data.get('model', '')}".strip(),
            "location": None  # TODO: GPS → 주소 변환
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

@app.get("/api/v1/photos/duplicates")
async def get_duplicates():
    """중복 사진 그룹 찾기"""
    
    if not blob_service_client:
        raise HTTPException(503, "Storage not configured")
    
    try:
        # 모든 사진 메타데이터 수집
        container_client = blob_service_client.get_container_client("uploads")
        blobs = list(container_client.list_blobs())
        
        photos_metadata = []
        
        for blob in blobs:
            # Blob 다운로드
            blob_client = container_client.get_blob_client(blob.name)
            blob_data = blob_client.download_blob().readall()
            
            # EXIF 추출
            exif_data = extract_exif_data(blob_data)
            
            if exif_data and exif_data.get('datetime'):
                photos_metadata.append({
                    'filename': blob.name,
                    'blob_name': blob.name,
                    'size': len(blob_data),
                    'datetime': exif_data.get('datetime'),
                    'gps': exif_data.get('gps'),
                    'url': blob_client.url
                })
        
        # 중복 그룹 찾기
        duplicate_groups = find_duplicate_groups(photos_metadata)
        
        # 응답 포맷팅
        response = {
            "total_groups": len(duplicate_groups),
            "total_duplicates": sum(len(group) for group in duplicate_groups),
            "groups": []
        }
        
        for i, group in enumerate(duplicate_groups):
            response["groups"].append({
                "group_id": f"group_{i+1}",
                "count": len(group),
                "time_range": {
                    "start": group[0]['datetime'],
                    "end": group[-1]['datetime']
                },
                "photos": [
                    {
                        "filename": p['filename'],
                        "datetime": p['datetime'],
                        "size": p['size'],
                        "gps": p['gps'],
                        "url": p['url']
                    }
                    for p in group
                ]
            })
        
        return response
        
    except Exception as e:
        raise HTTPException(500, f"Failed to find duplicates: {str(e)}")


@app.post("/api/v1/duplicates/organize")
async def organize_duplicates():
    """중복 사진들을 duplicates 컨테이너로 이동"""
    
    if not blob_service_client:
        raise HTTPException(503, "Storage not configured")
    
    try:
        # 중복 그룹 찾기
        duplicates_response = await get_duplicates()
        
        if duplicates_response['total_groups'] == 0:
            return {
                "message": "No duplicates found",
                "moved": 0
            }
        
        uploads_client = blob_service_client.get_container_client("uploads")
        
        # archive 컨테이너를 duplicates용으로 사용
        # (또는 새 컨테이너 생성)
        duplicates_client = blob_service_client.get_container_client("archive")
        
        moved_count = 0
        
        for group in duplicates_response['groups']:
            group_id = group['group_id']
            
            for photo in group['photos']:
                source_blob_name = photo['filename']
                dest_blob_name = f"{group_id}/{source_blob_name}"
                
                # 복사
                source_blob = uploads_client.get_blob_client(source_blob_name)
                dest_blob = duplicates_client.get_blob_client(dest_blob_name)
                
                dest_blob.start_copy_from_url(source_blob.url)
                
                # 원본은 유지 (삭제하려면 주석 해제)
                # source_blob.delete_blob()
                
                moved_count += 1
        
        return {
            "message": "Duplicates organized successfully",
            "total_groups": duplicates_response['total_groups'],
            "moved": moved_count
        }
        
    except Exception as e:
        raise HTTPException(500, f"Failed to organize duplicates: {str(e)}")    

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)