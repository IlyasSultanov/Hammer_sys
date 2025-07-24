import redis
from os import getenv

try:
    r = redis.Redis(
        host='redis',
        port=6379,
        password=getenv('REDIS_PASSWORD'),
        socket_connect_timeout=5
    )
    print("Redis ping:", r.ping())
except Exception as e:
    print("Redis connection error:", e)