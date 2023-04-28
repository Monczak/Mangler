import logging
import re

from pathlib import Path

import redis


logger = logging.getLogger("mangler")


class CacheManager:
    REDIS_REGEX = re.compile(r"^(?:.*://|)(.*):(.*)/.*$")

    def __init__(self, path, redis_url):
        self.path = Path(path)

        host, port = self.REDIS_REGEX.match(redis_url).groups()

        try:
            logger.info(f"Trying to connect to Redis at host {host} port {port}")
            self.redis = redis.Redis(host=host, port=int(port))
            self.redis.ping()
            logger.info("Connected to Redis")
        except redis.exceptions.ConnectionError as err:
            logger.error(f"Could not connect to Redis: {str(err)}")
            raise err

    class Acquire:
        def __init__(self, outer, file_name, mode):
            self._outer = outer
            self._file_name = file_name
            self._mode = mode
            self._file_obj = None
        
        # TODO: Implement locking with Redis
        def __enter__(self):
            cache_path = self._outer.path / self._file_name
            self._exists = cache_path.exists()

            if not self._exists:
                open(cache_path, "a").close()

            self._file_obj = open(cache_path, mode=self._mode)
            return self
        
        def __exit__(self, exc_type, exc_value, exc_tb):
            if self._file_obj:
                self._file_obj.close()

        @property
        def file(self):
            return self._file_obj
        
        @property
        def exists(self):
            return self._exists
        
    def acquire(self, file_name, mode):
        return self.Acquire(self, file_name, mode)

    


    