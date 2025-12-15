# Mini_Map

Web Flask tìm đường đi ngắn nhất trên bản đồ phường Lĩnh Nam bằng nhiều thuật toán, sử dụng Leaflet.js.

## Tính năng

- **Tìm đường** với nhiều thuật toán: Dijkstra, A*, BFS, DFS, Greedy, Bidirectional Dijkstra
- **Chọn phương tiện**: car, bicycle, foot (mỗi loại có tốc độ và đường cho phép khác nhau)
- **Đặt điều kiện đường**: jam (kẹt xe), flooded (ngập), construction (đang thi công), not allowed (cấm đi)
- **Hiển thị bản đồ** với Leaflet.js

## Cài đặt

### Yêu cầu
- Python 3.10+
- pip

### Tạo môi trường ảo
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python -m venv venv
source venv/bin/activate
```

### Cài đặt thư viện
```bash
pip install -r requirements.txt
```

## Chạy ứng dụng

### Cách 1: Dùng Flask CLI
```bash
flask run
```

### Cách 2: Chạy trực tiếp
```bash
python app.py
```

Mở trình duyệt và truy cập: **http://127.0.0.1:8000**

## Hướng dẫn sử dụng

### Tìm đường
1. Click vào bản đồ để chọn **điểm bắt đầu** (marker xanh lá)
2. Click lần 2 để chọn **điểm kết thúc** (marker đỏ)
3. Chọn **thuật toán** từ dropdown
4. Chọn **phương tiện** (car/bicycle/foot)
5. Nhấn **Find Path** để tìm đường

### Đặt điều kiện đường
1. Click vào một **con đường** trên bản đồ
2. Chọn điều kiện: normal, jam, flooded, construction, not allowed
3. Nhấn **Finalize Conditions** để áp dụng
4. Các đường "not allowed" sẽ bị loại khỏi tìm đường

### Reset
- **Clear Route**: Xóa đường đi hiện tại
- **Reset Weights**: Reset tất cả trọng số về mặc định

## Cấu trúc project

```
Mini_Map/
├── app.py                 # Entry point Flask app
├── config.py              # Cấu hình (paths, speeds, vehicles)
├── graph.py               # Build NetworkX graph từ GeoJSON
├── algorithms/            # Các thuật toán tìm đường
│   ├── dijkstra.py
│   ├── a_star.py
│   ├── bfs.py
│   ├── dfs.py
│   ├── greedy.py
│   └── bidirectional_dijkstra.py
├── condition/             # Xử lý điều kiện đường
│   ├── update_condition_temp.py
│   ├── finalize_condition.py
│   └── filter_routes.py
├── cache/                 # Cache điều kiện đường
│   └── condition_cache.py
├── routes/                # Flask routes
│   ├── map.py
│   └── algorithms.py
├── utils/                 # Utilities
│   ├── weighting.py
│   ├── reset_weights.py
│   └── sync_geojson.py
├── data/
│   ├── geojson/          # GeoJSON files (roads, weights, vhc_allowed)
│   └── graph/            # Graph pickle file
├── static/               # CSS, JS
└── templates/            # HTML templates
```

## API Endpoints

| Endpoint | Method | Mô tả |
|----------|--------|-------|
| `/` | GET | Trang chính |
| `/filter_routes` | POST | Lọc đường theo phương tiện |
| `/update_condition_temp` | POST | Cập nhật điều kiện tạm thời |
| `/finalize_conditions` | POST | Áp dụng điều kiện và rebuild graph |
| `/find_path` | POST | Tìm đường với thuật toán |
| `/reset` | POST | Reset weights về mặc định |

## License

MIT 
