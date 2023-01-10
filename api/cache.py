import time
from typing import Any

import loguru

from api.settings import settings


class Cache:

    __instance = None

    def __new__(cls):

        if not cls.__instance:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def __init__(self):

        self.__cache = dict()

    def set(self, key: str, value: Any, expired_at=settings.cache_default):

        if expired_at < 0:
            expired_at = 0

        self.__cache[key] = {
            'value': value,
            'expired_at': time.time() + expired_at,
        }

    def get(self, key: str) -> None:
        loguru.logger.info(self.__get(key))
        return self.__get(key)

    def update(self, key: str, value: list | Any):

        _value = self.__get(key)

        if not _value:
            return

        if isinstance(self.__cache[key]['value'], list):
            self.__cache[key]['value'].append(value)

        else:
            self.__cache[key]['value'] = value

    def delete(self, *keys):

        for key in keys:
            try:
                self.__cache.pop(key)
            except KeyError:
                pass

    def __get(self, key: str):

        value = self.__cache.get(key, None)

        if not value:
            return None

        if self.__is_expired(value['expired_at']):
            self.__cache.pop(key)
            return None

        return self.__cache[key]['value']

    @staticmethod
    def __is_expired(expired_at) -> bool:

        return int(expired_at) < int(time.time())

    def clear(self):

        self.__cache.clear()


cache = Cache()
