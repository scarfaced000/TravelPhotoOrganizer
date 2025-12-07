from pathlib import Path
import shutil
from typing import List, Dict

class AlbumOrganizer:
    def __init__(self, base_dir="./albums"):
        """앨범 관리자"""
        self.base_dir = Path(base_dir)
        self.base_dir.mkdir(exist_ok=True)
        
        # 하위 디렉토리
        self.location_dir = self.base_dir / "by_location"
        self.duplicate_dir = self.base_dir / "duplicates"
        
        self.location_dir.mkdir(exist_ok=True)
        self.duplicate_dir.mkdir(exist_ok=True)
    
    def organize_by_location(self, photos: List[Dict]) -> Dict:
        """장소별 앨범 생성"""
        organized = {}
        
        for photo in photos:
            location = photo.get('location_name', 'Unknown')
            
            # 장소별 폴더 생성
            location_folder = self.location_dir / self._sanitize_name(location)
            location_folder.mkdir(exist_ok=True)
            
            # 파일 복사
            source = Path(photo.get('storage_path'))
            if source.exists():
                dest = location_folder / source.name
                shutil.copy2(source, dest)
                
                if location not in organized:
                    organized[location] = []
                organized[location].append({
                    "filename": source.name,
                    "path": str(dest)
                })
        
        # 요약 정보
        summary = {
            "total_locations": len(organized),
            "albums": []
        }
        
        for location, files in organized.items():
            summary["albums"].append({
                "location": location,
                "photo_count": len(files),
                "folder_path": str(self.location_dir / self._sanitize_name(location))
            })
        
        return summary
    
    def organize_duplicates(self, duplicate_groups: List[List[Dict]]) -> Dict:
        """중복 사진 그룹별 폴더 생성"""
        organized = []
        
        for i, group in enumerate(duplicate_groups, 1):
            # 그룹 폴더 생성
            group_folder = self.duplicate_dir / f"group_{i}"
            group_folder.mkdir(exist_ok=True)
            
            files_copied = []
            for photo in group:
                source = Path(photo.get('storage_path'))
                if source.exists():
                    dest = group_folder / source.name
                    shutil.copy2(source, dest)
                    files_copied.append(source.name)
            
            organized.append({
                "group_id": i,
                "photo_count": len(files_copied),
                "folder_path": str(group_folder),
                "location": group[0].get('location_name', 'Unknown'),
                "datetime": group[0].get('datetime', 'Unknown')
            })
        
        return {
            "total_groups": len(organized),
            "groups": organized
        }
    
    def get_album_structure(self) -> Dict:
        """앨범 구조 조회"""
        structure = {
            "by_location": {},
            "duplicates": {}
        }
        
        # 장소별 앨범
        if self.location_dir.exists():
            for location_folder in self.location_dir.iterdir():
                if location_folder.is_dir():
                    photo_count = len(list(location_folder.glob("*")))
                    structure["by_location"][location_folder.name] = {
                        "photo_count": photo_count,
                        "path": str(location_folder)
                    }
        
        # 중복 그룹
        if self.duplicate_dir.exists():
            for group_folder in self.duplicate_dir.iterdir():
                if group_folder.is_dir():
                    photo_count = len(list(group_folder.glob("*")))
                    structure["duplicates"][group_folder.name] = {
                        "photo_count": photo_count,
                        "path": str(group_folder)
                    }
        
        return structure
    
    def _sanitize_name(self, name: str) -> str:
        """폴더명으로 사용 가능하도록 정리"""
        # 특수문자 제거
        invalid_chars = '<>:"/\\|?*'
        for char in invalid_chars:
            name = name.replace(char, '_')
        return name.strip()

album_organizer = AlbumOrganizer()
