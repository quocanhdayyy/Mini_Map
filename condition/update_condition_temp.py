from flask import Blueprint, request, jsonify
from cache.condition_cache import condition_cache, save_cache

update_bp = Blueprint('update_condition_temp',__name__)

VALID_CONDITIONS = ["normal", "jam", "flooded", "not allowed", "construction"]

@update_bp.route('/update_condition_temp', methods=['POST'])
def update_condition_temp():
    data = request.get_json()
    edge_id = data.get('edge_id')
    condition = data.get('condition')
    
    if not edge_id or condition not in VALID_CONDITIONS:
        return jsonify({"status": "error", "message": f"Thông tin không hợp lệ. Condition phải là: {VALID_CONDITIONS}"}), 400

    condition_cache[str(edge_id)] = condition
    # ✅ Lưu cache vào file để persist
    save_cache(condition_cache)
    
    return jsonify({"status": "success", "message": f"Đã ghi tạm điều kiện cho edge {edge_id}"}), 200

