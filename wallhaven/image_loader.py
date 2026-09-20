import os
import requests
from PyQt6.QtCore import QObject, QRunnable, QThreadPool, pyqtSignal, pyqtSlot
from PyQt6.QtGui import QPixmap
from wallhaven.cache import cache

USER_AGENT = "WallhavenDesktop/1.0"


class ImageLoadSignals(QObject):
    finished = pyqtSignal(str, QPixmap)  # url, pixmap
    error = pyqtSignal(str, str)         # url, error_msg


class ImageLoadTask(QRunnable):
    def __init__(self, url: str, is_thumb: bool = True):
        super().__init__()
        self.url = url
        self.is_thumb = is_thumb
        self.signals = ImageLoadSignals()
        self.setAutoDelete(True)

    @pyqtSlot()
    def run(self):
        try:
            # Check cache first
            pixmap = cache.get_pixmap(self.url, self.is_thumb)
            if pixmap and not pixmap.isNull():
                self.signals.finished.emit(self.url, pixmap)
                return

            # Check if local file
            if os.path.exists(self.url):
                lower = self.url.lower()
                if lower.endswith((".jpg", ".jpeg", ".png", ".webp", ".bmp")):
                    pm = QPixmap(self.url)
                    if pm and not pm.isNull():
                        self.signals.finished.emit(self.url, pm)
                        return
                elif lower.endswith((".mp4", ".webm", ".mkv")):
                    thumb_path = cache.get_video_thumb_path(self.url)
                    if thumb_path.exists() and thumb_path.stat().st_size > 0:
                        pm = QPixmap(str(thumb_path))
                        if pm and not pm.isNull():
                            self.signals.finished.emit(self.url, pm)
                            return
                    try:
                        import subprocess
                        cmd = [
                            "ffmpeg",
                            "-ss", "00:00:01",
                            "-i", self.url,
                            "-vframes", "1",
                            "-q:v", "2",
                            str(thumb_path),
                            "-y",
                        ]
                        res = subprocess.run(cmd, capture_output=True, timeout=5)
                        if res.returncode == 0 and thumb_path.exists():
                            pm = QPixmap(str(thumb_path))
                            if pm and not pm.isNull():
                                self.signals.finished.emit(self.url, pm)
                                return
                    except Exception:
                        pass

            # Download
            resp = requests.get(
                self.url,
                headers={"User-Agent": USER_AGENT},
                timeout=12
            )
            if resp.status_code == 200:
                data = resp.content
                cache.save_data(self.url, data, self.is_thumb)
                pm = QPixmap()
                if pm.loadFromData(data):
                    try:
                        self.signals.finished.emit(self.url, pm)
                    except RuntimeError:
                        pass
                else:
                    try:
                        self.signals.error.emit(self.url, "Failed to decode image")
                    except RuntimeError:
                        pass
            else:
                try:
                    self.signals.error.emit(self.url, f"HTTP {resp.status_code}")
                except RuntimeError:
                    pass
        except RuntimeError:
            pass
        except Exception as e:
            try:
                self.signals.error.emit(self.url, str(e))
            except Exception:
                pass


class AsyncImageLoader(QObject):
    image_loaded = pyqtSignal(str, QPixmap)
    image_failed = pyqtSignal(str, str)

    def __init__(self, max_threads: int = 6):
        super().__init__()
        self.cache = cache
        self.pool = QThreadPool()
        self.pool.setMaxThreadCount(max_threads)
        self._pending_urls: set[str] = set()

    def load_image(self, url: str, is_thumb: bool = True) -> bool:
        """
        Loads an image asynchronously.
        If already in cache, emits signal immediately and returns True.
        Otherwise schedules in background and returns False.
        """
        if not url:
            return False

        # Instant cache hit
        pm = cache.get_pixmap(url, is_thumb)
        if pm and not pm.isNull():
            self.image_loaded.emit(url, pm)
            return True

        if os.path.exists(url) and not url.lower().endswith((".mp4", ".webm", ".mkv")):
            pm = QPixmap(url)
            if pm and not pm.isNull():
                self.image_loaded.emit(url, pm)
                return True

        if url in self._pending_urls:
            return False

        self._pending_urls.add(url)
        task = ImageLoadTask(url, is_thumb)
        task.signals.finished.connect(self._on_success)
        task.signals.error.connect(self._on_error)
        self.pool.start(task)
        return False

    def _on_success(self, url: str, pixmap: QPixmap):
        self._pending_urls.discard(url)
        self.image_loaded.emit(url, pixmap)

    def _on_error(self, url: str, err: str):
        self._pending_urls.discard(url)
        self.image_failed.emit(url, err)


# Global singleton instance for thumbnail loading
loader = AsyncImageLoader(max_threads=8)
