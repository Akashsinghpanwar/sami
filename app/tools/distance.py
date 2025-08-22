# app/tools/distance.py
import json, math, os
from app.settings import PORTS_PATH

PORTS = None

def _load_ports():
    global PORTS
    if PORTS is not None:
        return PORTS
    if not os.path.exists(PORTS_PATH):
        raise FileNotFoundError(f"ports.json not found at {PORTS_PATH}")
    with open(PORTS_PATH, "r", encoding="utf-8") as f:
        PORTS = json.load(f)
    return PORTS

def _haversine_nm(lat1, lon1, lat2, lon2):
    R_km = 6371.0
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat/2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return (R_km * c) * 0.539957  # km -> nautical miles

def distance_nm(port_a: str, port_b: str) -> float:
    ports = _load_ports()
    a, b = ports.get(port_a.upper()), ports.get(port_b.upper())
    if not a or not b:
        raise ValueError(f"Unknown port(s): {port_a} or {port_b}. Add to ports.json")
    nm = _haversine_nm(a["lat"], a["lon"], b["lat"], b["lon"])
    return round(nm, 1)
