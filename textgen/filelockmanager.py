import abc
import logging
import re

from pathlib import Path

import redis
from redis_lock import Lock


logger = logging.getLogger("mangler")


class FileLockedError(Exception):
    def __init__(self, file_name=None, *args):
        super().__init__(*args)
        self.file_name = file_name


class FileLockManager:
    REDIS_REGEX = re.compile(r"^(?:.*://|)(.*):(.*)/.*$")

    def __init__(self, path, redis_url, lock_timeout=60):
        self.path = Path(path)
        self.lock_timeout = lock_timeout

        host, port = self.REDIS_REGEX.match(redis_url).groups()

        try:
            logger.info(f"Trying to connect to Redis at host {host} port {port}")
            self.redis = redis.Redis(host=host, port=int(port))
            self.redis.ping()
            logger.info("Connected to Redis")
        except redis.exceptions.ConnectionError as err:
            logger.error(f"Could not connect to Redis: {str(err)}")
            raise err

    class _AcquireBase(abc.ABC):
        def __init__(self, outer, file_name, blocking=False):
            self._outer = outer
            self._file_name = file_name

            self._lock = Lock(self._outer.redis, f"file:{file_name}")
            self._blocking = blocking

        @abc.abstractmethod
        def _on_enter(self):
            pass

        @abc.abstractmethod
        def _on_exit(self):
            pass
        
        def __enter__(self):
            logger.info(f"Acquiring lock for file {self._file_name}")
            self._cache_path = self._outer.path / self._file_name
            if self._lock.acquire(blocking=self._blocking):
                self._on_enter()
                return self
            else:
                raise FileLockedError(self._file_name)
            
        def __exit__(self, exc_type, exc_value, exc_tb):
            self._on_exit()
            if self._lock.locked():
                self._lock.release()

        @property
        def path(self):
            return self._cache_path
                
        @property
        def exists(self):
            return self._cache_path.exists()
    
    class Acquire(_AcquireBase):
        def _on_enter(self):
            return super()._on_enter()
        
        def _on_exit(self):
            return super()._on_exit()

    class AcquireOpen(_AcquireBase):
        def __init__(self, outer, file_name, mode, blocking):
            super().__init__(outer, file_name, blocking)
            self._mode = mode
            self._file_obj = None
        
        def _on_enter(self):
            if not self.exists:
                open(self._cache_path, "a").close()

            self._cache_path.touch()
            self._file_obj = open(self._cache_path, mode=self._mode)
        
        def _on_exit(self):
            if self._file_obj:
                self._file_obj.close()

        @property
        def file(self):
            return self._file_obj
        
    def acquire(self, file_name, blocking=False):
        return self.Acquire(self, file_name, blocking)
    
    def acquire_open(self, file_name, mode, blocking=False):
        return self.AcquireOpen(self, file_name, mode, blocking)
    