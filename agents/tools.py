from langchain_community.tools import tool
from stargaze.utils.weather import get_weather
from stargaze.utils.astronomy import get_moon_phase, get_sky_events
from datetime import datetime
import os
from stargaze.utils.satellite import get_satellite_passes


@tool
def fetch_weather(location: str, date_str: str) -> str:
    """Returns weather summary for a given location and date (YYYY-MM-DD)."""
    date = datetime.strptime(date_str, "%Y-%m-%d")
    data = get_weather(location, date)
    return data['summary'] if data else "No weather data available."

@tool
def fetch_moon_phase(date_str: str) -> str:
    """Returns moon phase for a given date (YYYY-MM-DD)."""
    date = datetime.strptime(date_str, "%Y-%m-%d")
    return get_moon_phase(date)

@tool
def fetch_sky_events(location: str, date_str: str) -> str:
    """Returns visible sky events for a location and date (YYYY-MM-DD)."""
    date = datetime.strptime(date_str, "%Y-%m-%d")
    events = get_sky_events(location, date)
    return "\n".join(events)

@tool
def fetch_satellite_passes(location: str, days: int = 3) -> str:
    """Returns visible satellite passes for a location over the next few days."""        
    return get_satellite_passes(location, days)
