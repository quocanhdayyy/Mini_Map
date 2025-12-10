from pathlib import Path

# Lấy thư mục gốc của project (nơi chứa app.py)
BASE_DIR = Path(__file__).resolve().parent

ROADS_FILE = BASE_DIR / 'data/geojson/roads.geojson'
WEIGHTS_FILE = BASE_DIR / 'data/geojson/weights.geojson'
VHC_ALLOWED_FILE = BASE_DIR / 'data/geojson/vhc_allowed.geojson'
GRAPH_PATH = BASE_DIR / 'data/graph/graph_data.pkl'

DEFAULT_WEIGHT=1.0

ALLOWED_HIGHWAYS = {
    "car": [
        "motorway", "motorway_link", "trunk", "trunk_link",
        "primary", "primary_link", "secondary", "tertiary", "tertiary_link",
        "residential", "service", "unclassified", "track",
        "default"
    ],
    "motor": [
        "trunk", "trunk_link",
        "primary", "primary_link", "secondary", "tertiary", "tertiary_link",
        "residential", "service", "unclassified", "track",
        "cycleway", "path", 
        "default"
    ],
    "foot": [
        "primary", "primary_link", "secondary", "tertiary", "tertiary_link",
        "residential", "service", "unclassified", "track",
        "footway", "path", "steps", "cycleway", "pedestrian", 
        "default"
    ]
}


CONDITION_SPEED_FACTORS= {
    "normal": 1.0,
    "jam": 0.3,
    "flooded": 0.5,
    "not allowed": 0.00000001,
    "construction": 0.2  # Đường đang sửa chữa - rất chậm
}
# nhân tốc độ xe theo loại đường với hệ số điều kiện->tốc độ của xe trong đkien đó
DEFAULT_SPEED_BY_VEHICLE = {
    "car": {
        "motorway": 100,
        "motorway_link": 60,
        "trunk": 80,
        "trunk_link": 50,
        "primary": 60,
        "primary_link": 40,
        "secondary": 50,
        "tertiary": 40,
        "tertiary_link": 35,
        "residential": 30,
        "service": 20,
        "unclassified": 30,
        "track": 20,
        "default": 40
    },
    "motor": {
        "trunk": 60,
        "trunk_link": 40,
        "primary": 50,
        "primary_link": 30,
        "secondary": 40,
        "tertiary": 35,
        "tertiary_link": 30,
        "residential": 25,
        "service": 20,
        "unclassified": 25,
        "track": 15,
        "cycleway": 20,
        "path": 15,
        "default": 30
    },
    "foot": {
        "primary": 4,          
        "primary_link": 3,
        "secondary": 4,
        "tertiary": 5,
        "tertiary_link": 5,
        "residential": 5,
        "service": 5,
        "unclassified": 4,
        "track": 4,
        "footway": 5,
        "path": 4,
        "steps": 2,
        "cycleway": 5,
        "pedestrian": 5,
        "default": 5
    }
}