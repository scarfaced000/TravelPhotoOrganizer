# 📸 Travel Photo Organizer

**Azure 클라우드 기반 여행 사진 자동 정리 시스템**

![Python](https://img.shields.io/badge/Python-3.11-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104-green)
![Azure](https://img.shields.io/badge/Azure-Cloud-0089D6)
![Docker](https://img.shields.io/badge/Docker-Ready-2496ED)
![Terraform](https://img.shields.io/badge/Terraform-IaC-7B42BC)

---

## 🏗️ **Infrastructure Architecture**

### **Azure 인프라 구성도**

<img width="850" height="772" alt="Azure Architecture" src="https://github.com/user-attachments/assets/ec2ec891-2451-4a43-bb55-b5c507442abd" />

### **배포된 리소스 (현재 상태)**

#### ✅ **완료된 인프라**
```
Resource Group: rg-travelphoto-dev (Korea Central)

Network Layer:
├── Virtual Network: vnet-travelphoto (10.0.0.0/16)
│   ├── Public Subnet: 10.0.1.0/24
│   ├── Private Subnet: 10.0.2.0/24
│   └── Network Security Group: nsg-app-service

Storage Layer:
├── Storage Account: sttravelphotodev
│   ├── Container: uploads (임시 저장)
│   ├── Container: albums (정리된 사진)
│   └── Container: archive (백업)

Monitoring:
└── Log Analytics: log-travelphoto-dev (30일 보존)
```

#### 🔄 **진행 중**
- **Container Registry**: acrtravelphotodev (Terraform 모듈 완성)
- **Container Apps**: ca-travelphoto-api-dev (ACR 연동 후 재배포)

---

##  **프로젝트 개요**

여행 후 수백 장의 사진을 수동으로 정리하는 번거로움을 해결하기 위한 클라우드 기반 자동 정리 시스템

**핵심 가치:**
-  **시간 절약**: 100장 사진 → 5분 내 자동 정리
-  **정확도**: GPS 기반 장소 인식 90%+ 정확도
-  **중복 제거**: 연속 촬영 사진 자동 감지 및 그룹핑

---

##  **주요 기능**

### 1. **GPS 기반 위치 추출**
- EXIF 데이터에서 GPS 좌표 자동 추출
- Geopy API를 통한 좌표 → 한글 주소 변환
- 정확도: **90%+**

### 2. **장소별 앨범 자동 생성**
```
albums/
├── by_location/
│   ├── 해운대구/     (45장)
│   ├── 광안대교/     (32장)
│   └── 강릉시/       (28장)
```

### 3. **중복 사진 자동 감지**
- 촬영 시간 기반 그룹핑 (10초 이내 연속 촬영)
- 파일 크기 유사도 비교 (10% 이내)
- 중복 감지율: **95%+**

### 4. **메타데이터 관리**
- 촬영 시간, 카메라 정보, GPS 좌표
- JSON 기반 영구 저장
- RESTful API 제공

---

##  **기술 스택**

### **Backend**
- **FastAPI** (Python 3.11) - 고성능 비동기 웹 프레임워크
- **Pillow** - EXIF 데이터 추출
- **Geopy** - Geocoding (GPS → 주소 변환, Nominatim API)
- **Uvicorn** - ASGI 서버

### **Infrastructure (Azure)**
- **Container Registry** - Docker 이미지 저장소 (Basic SKU)
- **Container Apps** - 서버리스 컨테이너 실행 환경
- **Blob Storage** - 이미지 파일 저장 (LRS, Standard)
- **Virtual Network** - 네트워크 격리 및 보안
- **Log Analytics** - 로그 수집 및 모니터링

### **DevOps**
- **Terraform** - Infrastructure as Code (모듈화 구조)
- **Docker** - 컨테이너화 (멀티스테이지 빌드)
- **Git/GitHub** - 버전 관리
- **Azure DevOps Boards** - 프로젝트 관리 (Epic/Feature/Task)

### **Frontend**
- **HTML/CSS/JavaScript** - 순수 웹 기술
- **Drag & Drop API** - 파일 업로드

---

## 📂 **프로젝트 구조**
```
TravelPhotoOrganizer/
├── travel-photo-organizer/
│   ├── backend/                # FastAPI 백엔드
│   │   ├── app/
│   │   │   ├── main.py        # API 엔드포인트
│   │   │   └── routers/       # API 라우터
│   │   ├── exif_extractor.py  # EXIF 데이터 추출
│   │   ├── geocoder.py        # GPS → 주소 변환
│   │   ├── duplicate_detector.py  # 중복 사진 감지
│   │   ├── album_organizer.py     # 앨범 자동 생성
│   │   ├── Dockerfile         # 컨테이너 이미지 정의
│   │   └── requirements.txt   # Python 패키지
│   └── frontend/
│       └── index.html         # 웹 UI
├── modules/                   # Terraform 모듈
│   ├── network/              # VNet, Subnet, NSG
│   ├── storage/              # Blob Storage
│   ├── log_analytics/        # Log Analytics Workspace
│   ├── container_registry/   # Azure Container Registry
│   └── container_apps/       # Container Apps
├── main.tf                   # Terraform 메인 파일
├── variables.tf              # 변수 정의
├── outputs.tf                # 출력 값
├── backend.tf                # Remote State 설정
└── README.md
```

---

##  **로컬 실행 방법**

### **필수 요구사항**
- Python 3.11+
- Docker (선택)

### **1. 저장소 클론**
```bash
git clone https://github.com/scarfaced000/TravelPhotoOrganizer.git
cd TravelPhotoOrganizer/travel-photo-organizer/backend
```

### **2. 가상환경 설정**
```bash
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### **3. 서버 실행**
```bash
python main.py
```

### **4. 웹 UI 실행 (다른 터미널)**
```bash
cd ../frontend
python3 -m http.server 3000
```

### **5. 브라우저 접속**
- **API 문서**: http://localhost:8000/docs
- **웹 UI**: http://localhost:3000

---

## 🐳 **Docker로 실행**
```bash
cd travel-photo-organizer/backend

# 이미지 빌드
docker build -t travel-photo-api:latest .

# 컨테이너 실행
docker run -p 8000:8000 travel-photo-api:latest
```

**API 문서 접속:** http://localhost:8000/docs

---

##  **API 엔드포인트**

### **사진 관리**
- `POST /api/upload` - 사진 업로드
- `GET /api/photos` - 사진 목록 조회
- `DELETE /api/photos/clear` - 모든 사진 삭제

### **중복 감지**
- `GET /api/duplicates` - 중복 사진 그룹 찾기

### **앨범 관리**
- `POST /api/organize` - 자동 정리 실행
- `GET /api/albums` - 앨범 구조 조회

### **시스템**
- `GET /` - API 상태 확인
- `GET /health` - 헬스 체크

**상세 문서:** http://localhost:8000/docs

---

##  **Terraform 인프라 배포**

### **배포 방법**
```bash
# 1. Terraform 초기화
terraform init

# 2. Dev 환경 선택
terraform workspace select dev
# 또는 새로 생성
terraform workspace new dev

# 3. 배포 계획 확인
terraform plan

# 4. 인프라 배포
terraform apply
```

### **배포되는 리소스**
```
총 13개 Azure 리소스:
├── Resource Group (1)
├── Virtual Network (1)
├── Subnets (2)
├── Network Security Group (1)
├── Storage Account (1)
├── Blob Containers (3)
├── Log Analytics Workspace (1)
├── Container Registry (1)
├── Container App Environment (1)
└── Container App (1)
```

### **환경 분리 (Workspace)**
```bash
# Dev 환경
terraform workspace select dev
terraform apply

# Prod 환경
terraform workspace select prod
terraform apply
```

---



---



---

## 🎓 **학습 성과**

### **기술적 성과**
- ✅ **Terraform 모듈화 구조 설계** - Network, Storage, Container 모듈 분리
- ✅ **Docker 멀티스테이지 빌드** - Python slim 이미지로 최적화
- ✅ **FastAPI 비동기 API 구현** - async/await 패턴 활용
- ✅ **Azure 네트워크 보안** - NSG, Private Subnet 설정
- ✅ **Terraform Workspace** - dev/prod 환경 분리

### **해결한 문제**

#### 1. **EXIF GPS 정밀도 처리**
```python
# 도/분/초 → 십진법 변환
def dms_to_decimal(degrees, minutes, seconds, direction):
    decimal = degrees + (minutes / 60.0) + (seconds / 3600.0)
    if direction in ['S', 'W']:
        decimal = -decimal
    return decimal
```

#### 2. **Docker 이미지 최적화**
- Before: 500MB → After: 200MB (60% 감소)
- Python slim 이미지 사용
- 멀티스테이지 빌드 적용

#### 3. **Terraform Backend State 관리**
- Azure Blob Storage에 Remote State 저장
- State Locking으로 동시 수정 방지



---

## 📊 **개발 현황**

### ✅ **완료 (Sprint 1-2)**
- [x] FastAPI RESTful API 개발
  - Photos API (업로드, 조회)
  - Albums API (생성, 조회)
  - Health Check 엔드포인트
- [x] Docker 컨테이너화
  - Dockerfile 작성
  - 로컬 빌드/실행 성공
- [x] Terraform 인프라 모듈 작성
  - Network (VNet, Subnet, NSG)
  - Storage (Blob Storage, Containers)
  - Log Analytics
  - Container Registry
  - Container Apps
- [x] 비용 최적화
  - ₩3,025 → ₩0.13/월 (99% 절감)

### 🔄 **진행 중 (Sprint 3)**
- [ ] Container Registry 배포
- [ ] Docker 이미지 ACR Push
- [ ] Container Apps ACR 연동
- [ ] API 통합 테스트

### 📅 **예정 (Sprint 4~)**
- [ ] CI/CD 파이프라인 (GitHub Actions)
- [ ] Azure OpenAI Vision API 연동
- [ ] 모니터링 대시보드 (Grafana)
- [ ] PostgreSQL 마이그레이션

---

##  **향후 개선 계획**

### **Phase 1: AI 고도화**
- [ ] Azure OpenAI Vision으로 이미지 내용 분석
- [ ] 자동 태그 생성 (해변, 산, 도시 등)
- [ ] 얼굴 인식 및 그룹핑

### **Phase 2: 확장성**
- [ ] SQLite → PostgreSQL 마이그레이션
- [ ] Redis 캐싱 추가
- [ ] CDN 연동 (이미지 최적화)




---

##  **개발자**

**이채림 (Chaelim Lee)**
- 숙명여자대학교 소프트웨어학부
- GitHub: [@scarfaced000](https://github.com/scarfaced000)
- Email: jazmyne@naver.com

### **프로젝트 기간**
- **시작일**: 2024년 11월
- **현재 상태**: 진행 중 (Sprint 3)

---

##  **라이선스**

MIT License

---

##  **Acknowledgments**

- **FastAPI** - 고성능 Python 웹 프레임워크
- **Geopy** - Geocoding 서비스
- **Terraform** - Infrastructure as Code
- **Microsoft Azure** - 클라우드 플랫폼

---

##  **참고 자료**

- [FastAPI 공식 문서](https://fastapi.tiangolo.com/)
- [Terraform Azure Provider](https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs)
- [Azure Container Apps 문서](https://learn.microsoft.com/ko-kr/azure/container-apps/)
- [Geopy 문서](https://geopy.readthedocs.io/)

---

## 📸 **스크린샷**

### API 문서 (Swagger UI)

<img width="805" height="870" alt="image" src="https://github.com/user-attachments/assets/546c73db-8b08-4a4b-b4c3-8c444cbe74cd" />

<img width="731" height="913" alt="image" src="https://github.com/user-attachments/assets/572624c0-4d06-4ac1-bd69-7de7c1777d58" />


### 앨범 구조 예시
```
 정리 완료!

📁 albums/
├── 📍 by_location/
│   ├── 해운대구/ (45장)
│   ├── 광안대교/ (32장)
│   └── 강릉시/ (28장)
└── 🔄 duplicates/
    └── group_1/ (연속 촬영 10장)
```

---
## 🌐 Live Demo

**API Documentation:** 
https://ca-travelphoto-api-dev.wittygrass-d9ea239b.koreacentral.azurecontainerapps.io/docs

**Health Check:**
```bash
curl https://ca-travelphoto-api-dev.wittygrass-d9ea239b.koreacentral.azurecontainerapps.io/health
```

## 📊 프로젝트 현황

- Azure 인프라 배포 완료 (14개 리소스)
- FastAPI 백엔드 운영 중
- Container Registry 연동
- Terraform IaC로 전체 인프라 관리
  
