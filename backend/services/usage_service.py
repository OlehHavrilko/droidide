import redis
from datetime import datetime

class UsageService:
    def __init__(self):
        self.redis = redis.Redis(host="localhost", port=6379, db=0)
        self.free_tier_limit = 30

    def check_usage(self, user_id: str) -> bool:
        today = datetime.utcnow().strftime("%Y-%m-%d")
        key = f"usage:{user_id}:{today}"
        usage = self.redis.get(key)
        return not usage or int(usage) < self.free_tier_limit

    def increment_usage(self, user_id: str):
        today = datetime.utcnow().strftime("%Y-%m-%d")
        key = f"usage:{user_id}:{today}"
        self.redis.incr(key)
        self.redis.expire(key, 86400)  # Expire in 24 hours
