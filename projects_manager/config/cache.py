import time
from typing import Any, Optional, Dict
from threading import Lock


class InMemoryCache:
    def __init__(self, expiration_time: int = 300):
        self.cache: Dict[str, Dict[str, Any]] = {}
        self.expiration_time = expiration_time
        self.lock = Lock()

    def get(self, key: str) -> Any:
        with self.lock:
            entry = self.cache.get(key)
            if entry and (time.time() - entry["timestamp"] < self.expiration_time):
                return entry["value"]
            elif entry:
                del self.cache[key]
            return None

    def set(self, key: str, value: Any):
        with self.lock:
            self.cache[key] = {"value": value, "timestamp": time.time()}

    def clear(self, key: Optional[str] = None):
        with self.lock:
            if key:
                self.cache.pop(key, None)
            else:
                self.cache.clear()
