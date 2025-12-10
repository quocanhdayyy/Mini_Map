from flask import Blueprint, request, jsonify
from config import WEIGHTS_FILE, VHC_ALLOWED_FILE, GRAPH_PATH
import json
from utils.weighting import update_weight_file
from graph import build_graph_from_geojson, save_graph
from utils.sync_geojson import sync_geojson_file
from cache.condition_cache import condition_cache
from geopy.distance import geodesic
from pathlib import Path

final_bp = Blueprint('finalize_conditions', __name__)

def calculate_distance(p1, p2):
    # p1, p2 là [lon, lat]
    return geodesic((p1[1], p1[0]), (p2[1], p2[0])).meters

def build_new_graph_from_weights(weights_file):
    return build_graph_from_geojson(weights_file, snap_threshold=1)

@final_bp.route('/finalize_conditions', methods=['POST'])
def finalize_conditions():
    data = request.get_json()
    vehicle = data.get("vehicle")

    if not vehicle:
        return jsonify({"status": "error", "message": "Thiếu phương tiện"}), 400
    
    print(f"[finalize_conditions] condition_cache hiện tại: {condition_cache}")
    
    try:
        with open(VHC_ALLOWED_FILE, 'r', encoding='utf-8') as f:
            geojson_data = json.load(f)

        new_features = []
        total_travel_time = 0
        total_length = 0

        for feature in geojson_data['features']:
            props = feature['properties']
            highway = props.get('highway', '')
            
            # ✅ Handle cả @id và id
            feature_id = props.get('id') or props.get('@id') or ''
            feature_id_str = str(feature_id)
            
            # Lấy condition từ cache, mặc định là "normal"
            condition_feature = condition_cache.get(feature_id_str, "normal")
            print(f"[finalize] Feature {feature_id_str}: condition = {condition_feature}")
            
            geometry = feature['geometry']

            coords_list = []
            if geometry['type'] == 'LineString':
                coords_list = [geometry['coordinates']]
            elif geometry['type'] == 'MultiLineString':
                coords_list = geometry['coordinates']
            else:
                continue  # không hỗ trợ

            # Tạo các đoạn nhỏ từ coords_list
            for line_coords in coords_list:
                for i in range(len(line_coords) - 1):
                    p1 = line_coords[i]
                    p2 = line_coords[i + 1]

                    segment_length = calculate_distance(p1, p2)
                    edge_id = f"{feature_id_str}_{i}"  # ✅ Dùng feature_id_str đã xử lý @id

                    # Lấy điều kiện cho đoạn này
                    condition = condition_feature

                    weight, speed_used, _ = update_weight_file(edge_id, segment_length, condition, highway, vehicle, condition_cache)

                    # Tạo feature mới cho đoạn nhỏ này
                    segment_feature = {
                        "type": "Feature",
                        "properties": {
                            "id": edge_id,
                            "vehicle": vehicle,
                            "condition": condition,
                            "speed": speed_used,
                            "weight": weight,
                            "length": segment_length,
                            "highway": highway
                        },
                        "geometry": {
                            "type": "LineString",
                            "coordinates": [p1, p2]
                        }
                    }
                    new_features.append(segment_feature)

                    total_travel_time += weight
                    total_length += segment_length

        # Ghi ra weights.geojson
        with open(WEIGHTS_FILE, 'w', encoding='utf-8') as f:
            json.dump({
                "type": "FeatureCollection",
                "features": new_features
            }, f, indent=2, ensure_ascii=False)

        print(f"[finalize_conditions] Ghi {len(new_features)} đoạn nhỏ vào weights.geojson")
        print(f"Tổng thời gian: {total_travel_time} giờ, Tổng chiều dài: {total_length} mét")

        # Xây dựng lại graph
        G_new = build_new_graph_from_weights(WEIGHTS_FILE)

        Path(GRAPH_PATH).parent.mkdir(parents=True, exist_ok=True)
        save_graph(G_new, GRAPH_PATH)

        sync_geojson_file('weights.geojson', force=True)

        return jsonify({
            "status": "success",
            "message": "Đã cập nhật xong weights.geojson",
            "total_travel_time": round(total_travel_time, 5),
            "total_length": round(total_length, 1)
        }), 200

    except Exception as e:
        print(f"[finalize_conditions] Lỗi: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500
