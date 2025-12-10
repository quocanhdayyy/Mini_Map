from flask import Blueprint, render_template, jsonify
from utils.reset_weights import reset_weights
from config import WEIGHTS_FILE

map_bp = Blueprint("map", __name__)

@map_bp.route("/")
def index():
    # Không reset weights mỗi lần load trang - tránh mất dữ liệu
    return render_template("index.html")

@map_bp.route("/reset", methods=["POST"])
def reset():
    """Endpoint riêng để reset weights khi user yêu cầu"""
    try:
        reset_weights(WEIGHTS_FILE)
        return jsonify({"status": "success", "message": "Đã reset weights thành công"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
