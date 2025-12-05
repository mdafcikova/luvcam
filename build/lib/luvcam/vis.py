
from __future__ import annotations

import math
from datetime import datetime
from typing import Dict, Iterable, List, Optional, Sequence, Union

import ephem
import ephem.stars
from scipy.spatial.transform import Rotation as R
import numpy as np
from .tle import _checksum

# ---------------------------------------------------------------------------
#  Internal helpers
# ---------------------------------------------------------------------------

def _checksum(line: str) -> int:
    """Return NORAD checksum (mod‑10) for first 68 chars of *line*."""
    s = 0
    for ch in line[:68]:
        if ch.isdigit():
            s += int(ch)
        elif ch == "-":
            s += 1
    return s % 10

def _clean_tle_line(line: str) -> str:
    """Strip extraneous chars and repair checksum to 69‑char TLE."""
    line = line.rstrip().rstrip(",")  # remove trailing comma if present
    if len(line) < 69:
        line = line.ljust(69)
    return line[:68] + str(_checksum(line))


def _sanitize_tle(tle: Iterable[str]) -> tuple[str, str, str]:
    """Return name, line1, line2 with valid checksums."""
    name, l1, l2 = tle
    return name.strip(), _clean_tle_line(l1), _clean_tle_line(l2)


def _clean_tle_line(line: str) -> str:
    """Strip extraneous chars and repair checksum to 69‑char TLE."""
    line = line.rstrip().rstrip(",")  # remove trailing comma if present
    if len(line) < 69:
        line = line.ljust(69)
    return line[:68] + str(_checksum(line))


def _sanitize_tle(tle: Iterable[str]) -> tuple[str, str, str]:
    """Return name, line1, line2 with valid checksums."""
    name, l1, l2 = tle
    return name.strip(), _clean_tle_line(l1), _clean_tle_line(l2)


def _get_star(name: str):
    """Return PyEphem star object or *None* if name not found."""
    try:
        return ephem.star(name)
    except (KeyError, ValueError):
        return None
    
    
# ---------------------------------------------------------------------------
#  Public API
# ---------------------------------------------------------------------------


def find_visible_stars(
    tle_lines: Sequence[str],
    obs_time: Union[str, datetime, ephem.Date],
    *,
    sun_avoid_deg: float = 90.0,
    limb_avoid_deg: float = 10.0,
) -> List[Dict[str, float]]:
    """Return all stars that satisfy Sun‑avoidance and limb‑clearance.

    Parameters
    ----------
    tle_lines
        (name, L1, L2) TLE triple.
    obs_time
        Observation epoch (string, *datetime*, or *ephem.Date*).
    sun_avoid_deg
        Minimum Sun–star separation angle (deg).
    limb_avoid_deg
        Minimum altitude of star above local horizon (deg).
    star_names
        Iterable of star names (PyEphem catalogue) to consider.

    Returns
    -------
    list of dict
        Each dict has ``{"name", "magnitude", "sun_sep_deg", "limb_clearance_deg"}``,
        sorted by increasing magnitude (brightest first). Empty list if
        no star meets the constraints.
    """

    # Normalise epoch -------------------------------------------------------
    date = ephem.Date(obs_time) if not isinstance(obs_time, ephem.Date) else obs_time

    # Sanitize TLE & propagate ---------------------------------------------
    name, l1, l2 = _sanitize_tle(tle_lines)
    sat = ephem.readtle(name, l1, l2)


    # Compute satellite sub‑point & altitude via a dummy Earth observer
    earth_obs = ephem.Observer()
    earth_obs.lat, earth_obs.lon, earth_obs.elevation = "0", "0", 0
    earth_obs.date = date
    sat.compute(earth_obs)
    #print(f"SAT RA: {sat.ra* (180 / math.pi)}, Dec: {sat.dec* (180 / math.pi)}")

    sat_lat = float(sat.sublat)
    sat_lon = float(sat.sublong)
    sat_alt_m = float(sat.elevation)

    # Observer located at spacecraft
    sat_obs = ephem.Observer()
    sat_obs.lat = sat_lat
    sat_obs.lon = sat_lon
    sat_obs.elevation = sat_alt_m
    sat_obs.date = date
    sat_obs.pressure = 0
    sat_obs.horizon = - (np.arcsin(ephem.earth_radius / (sat_alt_m + ephem.earth_radius)))
    print(sat_obs.horizon)
    
    # Sun position (topocentric)
    sun = ephem.Sun()
    sun.compute(sat_obs)
    #sat_sun_rising = sat_obs.next_setting(sun)
    #print(sat_sun_rising)

    # Moon position
    moon = ephem.Moon()
    moon.compute(sat_obs)

    visibles: List[Dict[str, float]] = []

    for item in ephem.stars.stars:
        star_obj = ephem.stars.stars[item]
        if star_obj is None:
            continue

        star_obj.compute(sat_obs)

        alt_deg = math.degrees(star_obj.alt)
        if alt_deg < limb_avoid_deg:
            continue  # Below limb clearance

        sun_sep_deg = math.degrees(float(ephem.separation(sun, star_obj)))
        if sun_sep_deg < sun_avoid_deg:
            continue  # Too close to Sun

        visibles.append({
            "name": item,
            "magnitude": star_obj.mag,
            "sun_sep_deg": round(sun_sep_deg, 2),
            "limb_clearance_deg": round(alt_deg, 2),
            "RA": round(star_obj.ra * (180 / np.pi), 4),
            "Dec": round(star_obj.dec * (180 / np.pi), 4)
        })

    visibles.append({
        "name": "Moon",
        "magnitude":  moon.mag,
        "sun_sep_deg": math.degrees(float(ephem.separation(sun, moon))),
        "limb_clearance_deg": round(math.degrees(moon.alt)),
        "RA": round(star_obj.ra * (180 / np.pi), 4),
        "Dec": round(star_obj.dec * (180 / np.pi), 4)
    })  

def find_visible_stars(
    tle_lines: Sequence[str],
    obs_time: Union[str, datetime, ephem.Date],
    *,
    sun_avoid_deg: float = 90.0,
    limb_avoid_deg: float = 10.0,
) -> List[Dict[str, float]]:
    """Return all stars that satisfy Sun‑avoidance and limb‑clearance.

    Parameters
    ----------
    tle_lines
        (name, L1, L2) TLE triple.
    obs_time
        Observation epoch (string, *datetime*, or *ephem.Date*).
    sun_avoid_deg
        Minimum Sun–star separation angle (deg).
    limb_avoid_deg
        Minimum altitude of star above local horizon (deg).
    star_names
        Iterable of star names (PyEphem catalogue) to consider.

    Returns
    -------
    list of dict
        Each dict has ``{"name", "magnitude", "sun_sep_deg", "limb_clearance_deg"}``,
        sorted by increasing magnitude (brightest first). Empty list if
        no star meets the constraints.
    """

    # Normalise epoch -------------------------------------------------------
    date = ephem.Date(obs_time) if not isinstance(obs_time, ephem.Date) else obs_time

    # Sanitize TLE & propagate ---------------------------------------------
    name, l1, l2 = _sanitize_tle(tle_lines)
    sat = ephem.readtle(name, l1, l2)

    # Compute satellite sub‑point & altitude via a dummy Earth observer
    earth_obs = ephem.Observer()
    earth_obs.lat, earth_obs.lon, earth_obs.elevation = "0", "0", 0
    earth_obs.date = date
    sat.compute(earth_obs)

    sat_lat = float(sat.sublat)
    sat_lon = float(sat.sublong)
    sat_alt_m = float(sat.elevation)

    # Observer located at spacecraft
    sat_obs = ephem.Observer()
    sat_obs.lat = sat_lat
    sat_obs.lon = sat_lon
    sat_obs.elevation = sat_alt_m
    sat_obs.date = date

    # Sun position (topocentric)
    sun = ephem.Sun()
    sun.compute(sat_obs)

    visibles: List[Dict[str, float]] = []

    for item in ephem.stars.stars:
        star_obj = ephem.stars.stars[item]
        if star_obj is None:
            continue

        star_obj.compute(sat_obs)

        alt_deg = math.degrees(star_obj.alt)
        if alt_deg < limb_avoid_deg:
            continue  # Below limb clearance

        sun_sep_deg = math.degrees(float(ephem.separation(sun, star_obj)))
        if sun_sep_deg < sun_avoid_deg:
            continue  # Too close to Sun

        visibles.append({
            "name": item,
            "magnitude": star_obj.mag,
            "sun_sep_deg": round(sun_sep_deg, 2),
            "limb_clearance_deg": round(alt_deg, 2),
            "RA":  round(star_obj.ra * (180 / np.pi), 4),
            "Dec": round(star_obj.dec * (180 / np.pi), 4)
        })

    # Moon position
    moon = ephem.Moon()
    moon.compute(sat_obs)

    visibles.append({
        "name": "Moon",
        "magnitude":  moon.mag,
        "sun_sep_deg": math.degrees(float(ephem.separation(sun, moon))),
        "limb_clearance_deg": round(math.degrees(moon.alt)),
        "RA": round(moon.ra * (180 / np.pi), 4),
        "Dec": round(moon.dec * (180 / np.pi), 4)
    }) 

 

    # Sort by apparent magnitude (ascending => brighter first)
    visibles.sort(key=lambda d: d["magnitude"])


    return visibles


# ---------------------------------------------------------------------------
#  Marianna's Code for computing Quaternions
# ---------------------------------------------------------------------------

def ra_dec_to_quaternion(ra_deg, dec_deg):
    """
    Converts RA, Dec in degrees to quaternion (pointing with -X axis)
    Returns quaternion [x, y, z, w]
    """

    ra_rad = np.radians(ra_deg)
    dec_rad = np.radians(dec_deg)

    target_vec = np.array([
        np.cos(dec_rad) * np.cos(ra_rad),
        np.cos(dec_rad) * np.sin(ra_rad),
        np.sin(dec_rad)
    ])

    x_body_eci = -target_vec  # -X axis points to target

    # arbitrary "up" direction
    ref = np.array([0.0, 0.0, 1.0])
    if np.abs(np.dot(x_body_eci, ref)) > 0.99:
        ref = np.array([0.0, 1.0, 0.0])  # pick another if parallel

    z_body_eci = np.cross(x_body_eci, ref)
    z_body_eci /= np.linalg.norm(z_body_eci)

    y_body_eci = np.cross(z_body_eci, x_body_eci)
    y_body_eci /= np.linalg.norm(y_body_eci)

    rot_matrix = np.column_stack((x_body_eci, y_body_eci, z_body_eci))    
    rot = R.from_matrix(rot_matrix)
    quat = rot.as_quat()

    return quat
