from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
import io

class ExifExtractor:
    @staticmethod
    def extract_exif(image_bytes):
        try:
            image = Image.open(io.BytesIO(image_bytes))
            exif_data = image._getexif()
            
            if not exif_data:
                return {
                    "gps": None,
                    "datetime": None,
                    "camera": None,
                    "message": "No EXIF data found"
                }
            
            extracted = {
                "gps": None,
                "datetime": None,
                "camera": None
            }
            
            for tag_id, value in exif_data.items():
                tag = TAGS.get(tag_id, tag_id)
                
                if tag == "GPSInfo":
                    extracted["gps"] = ExifExtractor._parse_gps(value)
                elif tag == "DateTime":
                    extracted["datetime"] = str(value)
                elif tag == "Model":
                    extracted["camera"] = str(value)
            
            return extracted
        
        except Exception as e:
            return {
                "gps": None,
                "datetime": None,
                "camera": None,
                "error": str(e)
            }
    
    @staticmethod
    def _parse_gps(gps_info):
        try:
            gps_data = {}
            for key in gps_info.keys():
                decode = GPSTAGS.get(key, key)
                gps_data[decode] = gps_info[key]
            
            if "GPSLatitude" in gps_data and "GPSLongitude" in gps_data:
                lat = ExifExtractor._convert_to_degrees(gps_data["GPSLatitude"])
                lon = ExifExtractor._convert_to_degrees(gps_data["GPSLongitude"])
                
                if gps_data.get("GPSLatitudeRef") == "S":
                    lat = -lat
                if gps_data.get("GPSLongitudeRef") == "W":
                    lon = -lon
                
                return {"latitude": lat, "longitude": lon}
            
            return None
        except Exception as e:
            return {"error": str(e)}
    
    @staticmethod
    def _convert_to_degrees(value):
        d, m, s = value
        return float(d) + float(m) / 60 + float(s) / 3600

exif_extractor = ExifExtractor()
