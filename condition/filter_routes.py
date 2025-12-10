from flask import Blueprint, request, jsonify
from config import ROADS_FILE, VHC_ALLOWED_FILE, ALLOWED_HIGHWAYS, GRAPH_PATH
import json
from utils.sync_geojson import sync_geojson_file
from graph import build_graph_from_geojson, save_graph

filter_bp = Blueprint('filter_routes',__name__)

@filter_bp.route('/filter_routes', methods=['POST'])
def filter_routes():
    data = request.get_json()
    vehicle = data.get('vehicle')
    print(f"Vehicle: {vehicle}")

    # Kiểm tra xem phương tiện có hợp lệ không
    if not vehicle or vehicle not in ALLOWED_HIGHWAYS:
        return jsonify({'status': 'error', 'message': 'Phương tiện không hợp lệ'}), 400

    # Lọc các đoạn đường phù hợp với phương tiện
    with open(ROADS_FILE, 'r', encoding='utf-8') as f:
        geojson_data = json.load(f)

    allowed_routes = []
    for idx, feature in enumerate(geojson_data['features']):
        props = feature['properties']
        highway = props.get('highway')
        
        if highway in ALLOWED_HIGHWAYS[vehicle]:
            # ✅ Handle @id hoặc id
            edge_id = props.get('id') or props.get('@id') or f"edge_{idx}"
            props['id'] = edge_id  # Đảm bảo luôn có key 'id'
            props['vehicle'] = vehicle
            props['condition'] = 'normal'
            allowed_routes.append(feature)
    
    # Lưu các đoạn đường được phép vào vhc_allowed.geojson
    with open(VHC_ALLOWED_FILE, 'w', encoding='utf-8') as f:
        json.dump({"type": "FeatureCollection", "features": allowed_routes}, f, indent=2, ensure_ascii=False) 

    # ✅ Sau khi ghi xong, đồng bộ sang static/
    sync_geojson_file('vhc_allowed.geojson')
    print(f"[filter_routes] Ghi {len(allowed_routes)} tuyến cho {vehicle}")

    # ✅ Build và SAVE graph
    G = build_graph_from_geojson(VHC_ALLOWED_FILE, snap_threshold=1)
    save_graph(G, GRAPH_PATH)

    return jsonify({'status': 'success', 'message': 'Đã lọc các đoạn đường cho phương tiện: ' + vehicle}), 200


