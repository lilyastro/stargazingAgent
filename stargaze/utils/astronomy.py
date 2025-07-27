from astral import moon
from geopy.geocoders import Nominatim
from skyfield.data import hipparcos
from skyfield.api import load, wgs84, Star
from datetime import datetime, timezone, date as DateType
from typing import List, Dict, Union
import numpy as np

# Load planetary ephemeris
planets = load('de421.bsp')
ts = load.timescale()
with load.open(hipparcos.URL) as f:
    star_df = hipparcos.load_dataframe(f)

def get_moon_phase(date: DateType) -> str:
    """Returns the moon phase for a given date.
    
    Args:
        date (datetime.date): The date for which to get the moon phase.
    
    Returns:
        str: Description of the moon phase.
    
    """
    phase = moon.phase(date)
    if phase < 7:
        desc = "Waxing Crescent"
    elif phase < 14:
        desc = "First Quarter"
    elif phase < 21:
        desc = "Waning Gibbous"
    else:
        desc = "New Moon"
    illumination = round((phase / 29) * 100)
    return f"{desc} ({illumination}% illumination)"

def get_visible_planets(lat: float, lon: float, date: DateType) -> List[str]:
    """Returns a list of visible planets for a given location and date.
    
    Args:
        
        lat (float): Latitude of the observer's location.
        lon (float): Longitude of the observer's location.
        date (datetime.date): The date for which to check visibility.
    
    Returns:
        List[str]: List of visible planets with their altitudes.
    """
    local_dt = datetime(date.year, date.month, date.day, 22, 0)
    utc_dt = local_dt.astimezone(timezone.utc)
    t = ts.from_datetime(utc_dt)

    earth = planets['earth']
    location = earth + wgs84.latlon(latitude_degrees=lat, longitude_degrees=lon)

    planet_keys = {
        'Mercury': 'mercury',
        'Venus': 'venus',
        'Mars': 'mars',
        'Jupiter': 'jupiter barycenter',
        'Saturn': 'saturn barycenter',
    }

    visible_planets = []
    for name, key in planet_keys.items():
        try:
            planet = planets[key]
            astrometric = location.at(t).observe(planet)
            try:
                alt, az, distance = astrometric.apparent().altaz()
            except ValueError as e:
                print(f"Failed to unpack altaz values: {e}")
                continue  # skip this star or planet            
            if alt.degrees > 10:
                visible_planets.append(f"{name} (altitude: {alt.degrees:.1f}°)")
        except KeyError:
            continue

    return visible_planets

def star_from_hipparcos_row(row) -> Star:
    """Create a Star object from a Hipparcos row.
    
    Args:
        row (pd.Series): A row from the Hipparcos DataFrame.
    Returns:
        Star: A Skyfield Star object.
    """
    ra_hours = row['ra_hours'] if 'ra_hours' in row else row['ra']
    dec_degrees = row['dec_degrees'] if 'dec_degrees' in row else row['dec']

    return Star(ra_hours=ra_hours, dec_degrees=dec_degrees)

def get_bright_stars(lat: float, lon: float, date: DateType) -> List[str]:
    """Returns a list of bright stars visible at a given location and date.
    
    Args:
        lat (float): Latitude of the observer's location.
        lon (float): Longitude of the observer's location.
        date (datetime.date): The date for which to check visibility.   
    Returns:
        List[str]: List of bright stars with their altitudes and magnitudes.
    """
    local_dt = datetime(date.year, date.month, date.day, 22, 0)
    utc_dt = local_dt.astimezone(timezone.utc)
    t = ts.from_datetime(utc_dt)

    earth = planets['earth']
    location = earth + wgs84.latlon(latitude_degrees=lat, longitude_degrees=lon)

    bright_stars = star_df[star_df['magnitude'] < 2.5]
    visible_stars = []

    for hip_id, row in bright_stars.iterrows():
        try:
            star = star_from_hipparcos_row(row)  # Make sure this returns a valid Star object
            alt, az, _ = location.at(t).observe(star).apparent().altaz()
        except Exception as e:
            print(f"Skipping star HIP {hip_id} due to error: {e}")
            continue  # Skip this star if anything goes wrong

    if alt.degrees > 10:
        visible_stars.append(f"HIP {hip_id} (alt {alt.degrees:.1f}°, mag {row['magnitude']:.1f})")
    return visible_stars

def get_nearby_stars_constellation(lat: float, lon: float, date: DateType, max_distance_deg: float = 10) -> List[Dict[str, Union[str, float]]]:
    """Returns stars near the zenith for a given location and date.
    
    Args:
        lat (float): Latitude of the observer's location.
        lon (float): Longitude of the observer's location.
        date (datetime.date): The date for which to check visibility.
        max_distance_deg (float): Maximum angular distance from zenith in degrees.
    
    Returns:
        List[Dict[str, Union[str, float]]]: List of stars
    """
    local_dt = datetime(date.year, date.month, date.day, 22, 0)
    utc_dt = local_dt.astimezone(timezone.utc)
    t = ts.from_datetime(utc_dt)

    observer = wgs84.latlon(latitude_degrees=lat, longitude_degrees=lon).at(t)
    
    # Get zenith position as a skyfield position object
    zenith = observer.from_altaz(alt_degrees=90, az_degrees=0)
    zenith_ra, zenith_dec, _ = zenith.radec()  # Correctly get RA and Dec

    # Convert zenith RA/Dec to unit vector for angular distance calc
    zenith_vec = np.array([
        np.cos(np.radians(zenith_dec.degrees)) * np.cos(np.radians(zenith_ra.hours * 15)),
        np.cos(np.radians(zenith_dec.degrees)) * np.sin(np.radians(zenith_ra.hours * 15)),
        np.sin(np.radians(zenith_dec.degrees))
    ])

    results = []
    bright_stars = star_df[star_df['magnitude'] < 3.5]

    for hip_id, row in bright_stars.iterrows():
        # Create Star from Hipparcos data columns
        star = Star(ra_hours=row['ra_hours'], dec_degrees=row['dec_degrees'])
        
        ra_deg = star.ra.hours * 15
        dec_deg = star.dec.degrees

        star_vec = np.array([
            np.cos(np.radians(dec_deg)) * np.cos(np.radians(ra_deg)),
            np.cos(np.radians(dec_deg)) * np.sin(np.radians(ra_deg)),
            np.sin(np.radians(dec_deg))
        ])

        cos_angle = np.clip(np.dot(zenith_vec, star_vec), -1.0, 1.0)
        angle_deg = np.degrees(np.arccos(cos_angle))
        name = row.get('proper_name') or f"HIP {hip_id}"


        if angle_deg <= max_distance_deg:
            results.append({
                "hip_id": hip_id,
                "name": name,
                "magnitude": row['magnitude'],
                "constellation": row.get('constellation', 'Unknown'),
                "angular_distance_deg": round(angle_deg, 2)
            })

    results.sort(key=lambda x: x['angular_distance_deg'])
    return results

def get_sky_events(location: str, date: DateType) -> List[Union[str, List[Dict[str, Union[str, float]]]]]:
    """Returns visible sky events for a location and date.
    
    Args:
        location (str): Name of the location (e.g., "Paris, France").
        date (datetime.date): The date for which to check sky events.
    
    Returns:
        List[Union[str, List[Dict[str, Union[str, float]]]]]: List of visible planets, bright stars, and nearby stars.
        """
    geolocator = Nominatim(user_agent="stargazing_app")
    loc = geolocator.geocode(location)
    if not loc:
        return ["Location not found."]

    lat, lon = loc.latitude, loc.longitude
    events: List[Union[str, List[Dict[str, Union[str, float]]]]] = []

    # Planets
    planets_visible = get_visible_planets(lat, lon, date)
    if planets_visible:
        events.append("🌌 Visible Planets:")
        for p in planets_visible:
            events.append(f" - {p}")
    else:
        events.append("No major planets visible at 10 PM.")

    # Bright Stars
    bright_stars = get_bright_stars(lat, lon, date)
    if bright_stars:
        events.append("✨ Bright Stars Visible (mag < 2.5):")
        for s in bright_stars[:5]:
            events.append(f" - {s}")
    else:
        events.append("No bright stars visible at 10 PM.")

    # Stars near Zenith
    nearby_stars = get_nearby_stars_constellation(lat, lon, date)
    events.append("✨ Stars Near Zenith:")
    for star in nearby_stars:
        events.append(f" - {star['name']} (mag {star['magnitude']}, dist {star['angular_distance_deg']}°)")

    return events
