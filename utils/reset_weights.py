import json
from graph import build_graph_from_geojson, save_graph
from config import GRAPH_PATH, DEFAULT_SPEED_BY_VEHICLE
from cache.condition_cache import clear_cache

def reset_weights(weights_file, vehicle="car"):
    """
    Reset toàn bộ weights.geojson về trạng thái mặc định:
    - condition = normal
    - speed = tốc độ mặc định theo loại đường và xe
    - weight = travel_time (giờ) = length / (speed * 1000)
    - vehicle = giá trị được truyền vào
    """
    with open(weights_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    reset_count = 0
    speed_config = DEFAULT_SPEED_BY_VEHICLE.get(vehicle, DEFAULT_SPEED_BY_VEHICLE.get("car", {}))

    for feature in data["features"]:
        props = feature.get("properties", {})
        length = props.get("length", 0)
        highway = props.get("highway", "default")
        
        # Lấy tốc độ theo loại đường
        speed = speed_config.get(highway, speed_config.get("default", 30))
        
        # Tính travel_time (giờ)
        travel_time = (length / 1000) / speed if speed > 0 else float('inf')
        
        props.update({
            "vehicle": vehicle,
            "condition": "normal",
            "speed": speed,
            "weight": round(travel_time, 5),
        })
        reset_count += 1

    with open(weights_file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    # Clear condition cache
    clear_cache()

    # Sau khi reset, build lại graph
    G = build_graph_from_geojson(weights_file)
    save_graph(G, GRAPH_PATH)
    print(f"Graph đã reset: {len(G.nodes)} nodes, {len(G.edges)} edges")

    return G
