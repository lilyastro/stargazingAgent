import requests
from datetime import datetime, timezone
from typing import List, Dict
from geopy.geocoders import Nominatim
import os


# Popular satellites to check
SATELLITES = {
    25544: "International Space Station (ISS)",
    20580: "Hubble Space Telescope", 
    48274: "Tiangong Space Station",
    27424: "Aqua",
    25994: "Terra",
    39084: "Landsat 8",
    28654: "NOAA 18",
    33591: "NOAA 19",
}

def get_satellite_passes(location: str, days: int = 3, min_visibility: int = 300) -> str:
    """Get visible satellite passes for a location.
    
    Args:
        location (str): Location name (e.g., "New York, USA").
        days (int): Number of days to check for passes.
        min_visibility (int): Minimum visibility in seconds to consider a pass visible.
    
    Returns:
        str: Formatted string with visible satellite passes.
    
    """

    api_key = os.getenv('N2YO_API_KEY')
    
    if not api_key:
        return "Error: N2YO API key not configured. Get a free key at https://www.n2yo.com/api/"
    
    try:
        # Geocode location
        geolocator = Nominatim(user_agent="stargazing_agent")
        location_data = geolocator.geocode(location, timeout=10)
        if not location_data:
            return f"Could not find coordinates for location: {location}"
        
        latitude, longitude = location_data.latitude, location_data.longitude
        
        # Check each satellite
        visible_satellites = []
        for satellite_id, satellite_name in SATELLITES.items():
            try:
                url = f"https://api.n2yo.com/rest/v1/satellite/visualpasses/{satellite_id}/{latitude}/{longitude}/0/{min(days, 10)}/{min_visibility}&apiKey={api_key}"
                
                response = requests.get(url, timeout=10)
                response.raise_for_status()
                data = response.json()
                print(data)
                
                if 'error' not in data and data.get('passes'):
                    passes = data['passes']
                    visible_satellites.append({
                        'name': satellite_name,
                        'passes': passes[:3]  # Limit to 3 passes per satellite
                    })
                    
            except Exception:
                continue  # Skip satellites that error out
        
        return format_satellite_results(visible_satellites, location, latitude, longitude)
        
    except Exception as e:
        return f"Error getting satellite passes: {str(e)}"


def format_satellite_results(satellites: List[Dict], location: str, lat: float, lng: float) -> str:
    """Format satellite pass results.
    
    Args:
        satellites (List[Dict]): List of visible satellites with their passes.
        location (str): Location name.
        lat (float): Latitude of the location.
        lng (float): Longitude of the location.
    
    Returns:
        str: Formatted string with satellite pass details.
    """
    
    if not satellites:
        return f"🛰️ No visible satellite passes found from {location} in the next few days."
    
    result = f"🛰️ Visible satellites from {location}:\n"
    result += f"📍 {lat:.3f}°, {lng:.3f}°\n\n"
    
    for sat in satellites:
        result += f"{'─' * 40}\n"
        result += f"🛰️ {sat['name']}\n"
        result += f"{'─' * 40}\n"
        
        for i, pass_data in enumerate(sat['passes'], 1):
            start_time = datetime.fromtimestamp(pass_data['startUTC'], tz=timezone.utc)
            end_time = datetime.fromtimestamp(pass_data['endUTC'], tz=timezone.utc)
            duration = pass_data['duration']
            max_elevation = pass_data['maxEl']
            
            result += f"Pass #{i}:\n"
            result += f"  📅 {start_time.strftime('%Y-%m-%d')}\n"
            result += f"  🕐 {start_time.strftime('%H:%M')} - {end_time.strftime('%H:%M')} UTC\n"
            result += f"  ⏱️ {duration//60}m {duration%60}s\n"
            result += f"  📐 Max elevation: {max_elevation}°\n"
            result += f"  ✨ Magnitude: {pass_data.get('mag', 'N/A')}\n\n"
    
    # Generate Static Tips
    result += "💡 Tips:\n"
    result += "- ISS is usually the brightest and easiest to spot\n"
    result += "- Higher elevation passes are more visible\n"
    result += "- Best viewing during twilight hours\n"
    
    return result