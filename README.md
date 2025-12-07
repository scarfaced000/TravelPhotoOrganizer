# 📸 Travel Photo Organizer

Azure 기반 여행 사진 자동 정리 시스템

## 🚀 Quick Start
```bash
# 백엔드 실행
cd travel-photo-organizer/backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python main.py

# 프론트엔드 실행 (다른 터미널)
cd travel-photo-organizer/frontend
python3 -m http.server 3000
```

**접속:** http://localhost:3000

## 📖 문서

상세 문서는 [`travel-photo-organizer/README.md`](./travel-photo-organizer/README.md) 참조

## 🏗️ Infrastructure

Terraform 코드로 Azure 인프라 자동 배포
```bash
cd terraform
terraform init
terraform apply
```

## ⭐ 주요 기능

- ✅ GPS 기반 장소 자동 추출
- ✅ 중복 사진 자동 감지
- ✅ 장소별 앨범 자동 생성
- ✅ Docker 컨테이너화
- ✅ Terraform IaC

---

**Developer:** 이채림 | **GitHub:** [@scarfaced000](https://github.com/scarfaced000)
