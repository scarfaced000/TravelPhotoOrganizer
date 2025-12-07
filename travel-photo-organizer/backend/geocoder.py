from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderServiceError
import time

class GeocoderService:
    def __init__(self):
        self.geolocator = Nominatim(user_agent="travel-photo-organizer")
    
    def get_location_name(self, latitude: float, longitude: float):
        try:
            time.sleep(1)
            
            location = self.geolocator.reverse(f"{latitude}, {longitude}", language='ko')
            
            if location:
                address = location.raw.get('address', {})
                location_name = self._extract_location_name(address)
                
                return {
                    "display_name": location.address,
                    "location_name": location_name,
                    "address": address,
                    "latitude": latitude,
                    "longitude": longitude
                }
            
            return None
        
        except (GeocoderTimedOut, GeocoderServiceError) as e:
            print(f"Geocoding error: {e}")
            return {"error": str(e)}
    
    def _extract_location_name(self, address: dict):
        if 'tourism' in address:
            return address['tourism']
        elif 'suburb' in address:
            return address['suburb']
        elif 'city_district' in address:
            return address['city_district']
        elif 'city' in address:
            return address['city']
        else:
            return address.get('display_name', 'Unknown')

geocoder = GeocoderService()
