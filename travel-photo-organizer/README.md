# 📸 Travel Photo Organizer

여행 사진을 GPS 정보 기반으로 자동 정리하는 클라우드 기반 서비스

## ✨ 주요 기능

- 📍 **GPS 자동 추출**: EXIF 데이터에서 GPS 좌표 추출
- �� **장소명 변환**: GPS → 한글 주소 자동 변환
- 📅 **메타데이터 관리**: 촬영 시간, 카메라 정보 추출
- 🖼️ **드래그 앤 드롭**: 직관적인 웹 UI

## 🛠️ 기술 스택

**Backend**
- FastAPI (Python)
- Pillow (EXIF 추출)
- Geopy (Geocoding)

**Frontend**
- HTML/CSS/JavaScript
- Drag & Drop API

**Infrastructure**
- Azure Blob Storage
- Terraform (IaC)
- Docker

## 🚀 로컬 실행

\`\`\`bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python main.py
\`\`\`

## 📊 프로젝트 성과

- ✅ EXIF 데이터 추출 성공률: 95%+
- ✅ GPS → 장소명 변환 정확도: 90%+
- ✅ Azure 인프라 자동화 (Terraform)

## 👤 개발자

이채림 - [GitHub](https://github.com/chaelimjlee)
