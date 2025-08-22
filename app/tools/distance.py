import json
import os
from math import radians, cos, sin, asin, sqrt
from llama_index.core.tools import FunctionTool

_PORTS_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
    "data",
    "ports.json"
)
_PORTS = None

def _load_ports():
    global _PORTS
    if _PORTS is None:
        with open(_PORTS_PATH, "r") as f:
            _PORTS = {p["name"].lower(): (p["lat"], p["lng"]) for p in json.load(f)}

def _haversine(lat1, lon1, lat2, lon2):
    """Calculate the great-circle distance between two points on the earth."""
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * asin(sqrt(a))
    r = 3440  # Radius of Earth in nautical miles
    return c * r

def distance_nm(port_a: str, port_b: str) -> float:
    """
    Calculates the great-circle (shortest) distance between two ports in nautical miles.

    Args:
        port_a (str): The name of the first port.
        port_b (str): The name of the second port.
    """
    _load_ports()
    port_a_key = port_a.lower()
    port_b_key = port_b.lower()

    if port_a_key not in _PORTS:
        return f"Error: Port '{port_a}' not found."
    if port_b_key not in _PORTS:
        return f"Error: Port '{port_b}' not found."

    lat1, lon1 = _PORTS[port_a_key]
    lat2, lon2 = _PORTS[port_b_key]

    distance = _haversine(lat1, lon1, lat2, lon2)
    return round(distance, 2)

distance_tool = FunctionTool.from_defaults(
    fn=distance_nm,
    name="port_distance_calculator",
    description="Calculates the great-circle distance between two ports in nautical miles.",
)
