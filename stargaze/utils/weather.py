import requests
from datetime import datetime, date as DateType
from geopy.geocoders import Nominatim
from typing import Optional, Tuple, Dict, Union


def get_coords(location: str) -> Tuple[float, float]:
    """
    Converts a location string into latitude and longitude coordinates using geopy.

    Args:
        location (str): The name of the location (e.g., "Paris, France").

    Returns:
        Tuple[float, float]: A tuple containing (latitude, longitude).
    """
    geolocator = Nominatim(user_agent="stargazing_app")
    loc = geolocator.geocode(location)
    if not loc:
        raise ValueError(f"Location '{location}' not found.")
    return loc.latitude, loc.longitude


def get_weather(location: str, date: DateType) -> Optional[Dict[str, str]]:
    """
    Fetches weather forecast for a given location and date using the Open-Meteo API.
    Returns average cloud cover and temperature summary.

    Args:
        location (str): Name of the location (e.g., "London, UK").
        date (datetime.date): The date for which to fetch weather data.

    Returns:
        Optional[Dict[str, str]]: A dictionary with a summary string, or None if data is unavailable.
    """
    lat, lon = get_coords(location)

    # Format date to string as required by Open-Meteo API
    day_str = date.strftime("%Y-%m-%d")

    # Construct Open-Meteo API URL
    url = (
        f"https://api.open-meteo.com/v1/forecast"
        f"?latitude={lat}&longitude={lon}"
        f"&hourly=cloudcover,temperature_2m"
        f"&timezone=auto"
        f"&start_date={day_str}&end_date={day_str}"
    )

    # Fetch weather data
    res = requests.get(url).json()

    # Handle case where API doesn't return hourly data
    if 'hourly' not in res:
        return None

    hours = res['hourly']['time']
    clouds = res['hourly']['cloudcover']
    temps = res['hourly']['temperature_2m']

    # Compute average cloud cover and use first temperature reading as approximation
    avg_cloud = sum(clouds) / len(clouds) if clouds else None
    first_temp = temps[0] if temps else None

    if avg_cloud is None or first_temp is None:
        return None

    summary = f"{round(avg_cloud)}% cloud cover, Temp ~{round(first_temp)}°C"
    return {"summary": summary}
