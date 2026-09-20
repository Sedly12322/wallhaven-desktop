import hashlib
import os
import sys
from pathlib import Path
from typing import Optional
from PyQt6.QtGui import QPixmap

if sys.platform == "win32":
    localapp = os.environ.get("LOCALAPPDATA", str(Path.home() / "AppData" / "Local"))
    CACHE_DIR = Path(localapp) / "wallhaven-desktop"
else:
    CACHE_DIR = Path.home() / ".cache" / "wallhaven-desktop"
THUMB_CACHE_DIR = CACHE_DIR / "thumbnails"
FULL_CACHE_DIR = CACHE_DIR / "previews"

MAX_CACHE_BYTES = 500 * 1024 * 1024  # 500 MB


class ImageCache:
    def __init__(self):
        THUMB_CACHE_DIR.mkdir(parents=True, exist_ok=True)
        FULL_CACHE_DIR.mkdir(parents=True, exist_ok=True)
        self._pixmap_mem_cache: dict[str, QPixmap] = {}
        self._max_mem_entries = 120

    def _url_to_path(self, url: str, is_thumb: bool = True) -> Path:
        hash_str = hashlib.sha256(url.encode("utf-8")).hexdigest()
        ext = os.path.splitext(url.split("?")[0])[1] or ".jpg"
        target_dir = THUMB_CACHE_DIR if is_thumb else FULL_CACHE_DIR
        return target_dir / f"{hash_str}{ext}"

    def get_cached_path(self, url: str, is_thumb: bool = True) -> Optional[Path]:
        path = self._url_to_path(url, is_thumb)
        if path.exists() and path.stat().st_size > 0:
            return path
        return None

    def get_pixmap(self, url: str, is_thumb: bool = True) -> Optional[QPixmap]:
        if url in self._pixmap_mem_cache:
            return self._pixmap_mem_cache[url]

        path = self.get_cached_path(url, is_thumb)
        if path:
            pm = QPixmap(str(path))
            if not pm.isNull():
                if len(self._pixmap_mem_cache) >= self._max_mem_entries:
                    # Drop first 20 items
                    for k in list(self._pixmap_mem_cache.keys())[:20]:
                        del self._pixmap_mem_cache[k]
                self._pixmap_mem_cache[url] = pm
                return pm
        return None

    def save_data(self, url: str, data: bytes, is_thumb: bool = True) -> Path:
        path = self._url_to_path(url, is_thumb)
        try:
            temp_path = path.with_suffix(".tmp")
            with open(temp_path, "wb") as f:
                f.write(data)
            temp_path.replace(path)
            # Store in mem cache
            pm = QPixmap()
            if pm.loadFromData(data):
                if len(self._pixmap_mem_cache) >= self._max_mem_entries:
                    for k in list(self._pixmap_mem_cache.keys())[:20]:
                        del self._pixmap_mem_cache[k]
                self._pixmap_mem_cache[url] = pm
        except Exception as e:
            print(f"Error saving cached image {url}: {e}")
        return path

    def clean_old_cache_if_needed(self):
        try:
            total_size = sum(f.stat().st_size for f in CACHE_DIR.glob("**/*") if f.is_file())
            if total_size > MAX_CACHE_BYTES:
                files = sorted(
                    [f for f in CACHE_DIR.glob("**/*") if f.is_file()],
                    key=lambda f: f.stat().st_mtime
                )
                for f in files:
                    if total_size <= MAX_CACHE_BYTES * 0.7:
                        break
                    try:
                        total_size -= f.stat().st_size
                        f.unlink()
                    except Exception:
                        pass
        except Exception as e:
            print(f"Error cleaning cache: {e}")

    def get_video_thumb_path(self, video_path: str) -> Path:
        hash_str = hashlib.sha256(str(video_path).encode("utf-8")).hexdigest()
        return THUMB_CACHE_DIR / f"vid_{hash_str}.jpg"


cache = ImageCache()
