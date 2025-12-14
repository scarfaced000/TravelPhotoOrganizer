# Travel Photo Organizer - FastAPI Backend

Azure Container Apps에 배포되는 FastAPI 기반 백엔드 서비스

## 🚀 Features

- RESTful API (FastAPI)
- Azure Blob Storage 연동
- Health check endpoint
- CORS 지원
- OpenAPI/Swagger 자동 문서화

## 📦 API Endpoints

### Health Check
```
GET /health
```

### Photos
```
GET  /api/v1/photos          # List photos
POST /api/v1/photos/upload   # Upload photo
```

### Albums
```
GET  /api/v1/albums          # List albums
POST /api/v1/albums          # Create album
GET  /api/v1/albums/{id}     # Get album
```

## 🏃 Local Development

### Prerequisites
- Python 3.11+
- Docker (optional)

### Run with Python
```bash
# Install dependencies
pip install -r requirements.txt

# Set environment variables
export ENVIRONMENT=dev
export STORAGE_ACCOUNT_NAME=sttravelphotodev
export AZURE_REGION=koreacentral

# Run the app
python -m uvicorn app.main:app --reload
```

### Run with Docker
```bash
# Build image
docker build -t travel-photo-api:latest .

# Run container
docker run -d \
  -p 8000:8000 \
  -e ENVIRONMENT=dev \
  -e STORAGE_ACCOUNT_NAME=sttravelphotodev \
  -e AZURE_REGION=koreacentral \
  --name travel-photo-api \
  travel-photo-api:latest
```

## 📚 API Documentation

실행 후 접속:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 🌐 Environment Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `ENVIRONMENT` | 환경 (dev/prod) | `dev` |
| `STORAGE_ACCOUNT_NAME` | Azure Storage Account | `sttravelphotodev` |
| `AZURE_REGION` | Azure Region | `koreacentral` |

## 🐳 Docker Hub / ACR

```bash
# Tag for ACR
docker tag travel-photo-api:latest <acr-name>.azurecr.io/travel-photo-api:latest

# Push to ACR
docker push <acr-name>.azurecr.io/travel-photo-api:latest
```
