from datetime import datetime, timedelta
from typing import List, Dict
import os

class DuplicateDetector:
    def __init__(self, time_threshold_seconds=10):
        """
        중복 사진 감지기
        time_threshold_seconds: 연속 촬영으로 간주할 시간 간격 (초)
        """
        self.time_threshold = timedelta(seconds=time_threshold_seconds)
    
    def find_duplicates(self, photos: List[Dict]) -> List[List[Dict]]:
        """
        촬영 시간 기반 중복 사진 그룹핑
        
        Args:
            photos: 사진 정보 리스트 [{"filename": "...", "datetime": "...", "file_id": "..."}, ...]
        
        Returns:
            중복 그룹 리스트 [[photo1, photo2], [photo3, photo4, photo5], ...]
        """
        if not photos or len(photos) < 2:
            return []
        
        # 촬영 시간으로 정렬
        sorted_photos = sorted(
            photos, 
            key=lambda x: x.get('datetime', '9999:12:31 23:59:59')
        )
        
        groups = []
        current_group = [sorted_photos[0]]
        
        for photo in sorted_photos[1:]:
            if self._is_similar(current_group[-1], photo):
                current_group.append(photo)
            else:
                # 그룹이 2장 이상이면 중복으로 판단
                if len(current_group) > 1:
                    groups.append(current_group)
                current_group = [photo]
        
        # 마지막 그룹 처리
        if len(current_group) > 1:
            groups.append(current_group)
        
        return groups
    
    def _is_similar(self, photo1: Dict, photo2: Dict) -> bool:
        """두 사진이 중복인지 판단 (시간 + 파일크기 기반)"""
        
        # 1. 촬영 시간 비교
        time1 = photo1.get('datetime')
        time2 = photo2.get('datetime')
        
        if not time1 or not time2:
            return False
        
        try:
            dt1 = datetime.strptime(time1, "%Y:%m:%d %H:%M:%S")
            dt2 = datetime.strptime(time2, "%Y:%m:%d %H:%M:%S")
            
            time_diff = abs(dt2 - dt1)
            
            # 시간 차이가 threshold 이내
            if time_diff <= self.time_threshold:
                # 2. 파일 크기 비교 (옵션)
                size1 = photo1.get('size', 0)
                size2 = photo2.get('size', 0)
                
                if size1 and size2:
                    # 파일 크기 차이가 10% 이내면 유사
                    size_diff_ratio = abs(size1 - size2) / max(size1, size2)
                    return size_diff_ratio < 0.1
                
                return True
            
            return False
        
        except Exception as e:
            print(f"Error comparing photos: {e}")
            return False
    
    def get_duplicate_summary(self, groups: List[List[Dict]]) -> Dict:
        """중복 그룹 요약 정보"""
        total_photos = sum(len(group) for group in groups)
        total_groups = len(groups)
        
        # 각 그룹별 정보
        group_details = []
        for i, group in enumerate(groups, 1):
            group_details.append({
                "group_id": i,
                "count": len(group),
                "first_photo": group[0].get('filename'),
                "datetime": group[0].get('datetime'),
                "location": group[0].get('location_name', 'Unknown')
            })
        
        return {
            "total_duplicate_photos": total_photos,
            "duplicate_groups": total_groups,
            "groups": group_details
        }

duplicate_detector = DuplicateDetector()
