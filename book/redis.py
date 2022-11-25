import redis
from django.conf import settings


class RedisCode:

    def __init__(self):
        self.r = redis.Redis(**settings.REDIS_CONF)

    def extract(self, key):
        return self.r.get(key)

    def save(self, key, value):
        return self.r.set(key, value)
