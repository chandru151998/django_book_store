import redis


class RedisCode:

    def __init__(self):
        self.r = redis.Redis(host='localhost', port=6379)

    def extract(self, key):
        return self.r.get(key)

    def save(self, key, value):
        return self.r.set(key, value)
