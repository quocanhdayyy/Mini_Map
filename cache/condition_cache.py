# Cache module for condition data với persistence
import json
from pathlib import Path

# Lấy thư mục gốc của project
BASE_DIR = Path(__file__).resolve().parent.parent
CACHE_FILE = BASE_DIR / 'cache/condition_data.json'

def load_cache():
    """Load cache từ file nếu tồn tại"""
    if CACHE_FILE.exists():
        try:
            with open(CACHE_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_cache(cache_data):
    """Lưu cache vào file"""
    CACHE_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(CACHE_FILE, 'w', encoding='utf-8') as f:
        json.dump(cache_data, f, indent=2, ensure_ascii=False)

def clear_cache():
    """Xóa toàn bộ cache"""
    global condition_cache
    condition_cache = {}
    if CACHE_FILE.exists():
        CACHE_FILE.unlink()

# Load cache khi import module
condition_cache = load_cache()