import hashlib
import redis


class Cache:
    """
    Redis-based cache mechanism for storing product prices.
    """
    def __init__(self, redis_url: str = "redis://localhost:6379/0"):
        self.redis = redis.Redis.from_url(redis_url)

    def get(self, key: str):
        value = self.redis.get(key)
        return value.decode() if value else None

    def set(self, key: str, value: str):
        self.redis.set(key, value)

    def generate_key(self, product_title: str) -> str:
        """
        Generate a unique key for a product title.
        """
        return hashlib.md5(product_title.encode()).hexdigest()
