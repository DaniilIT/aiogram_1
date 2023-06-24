from config import REDIS_HOST, REDIS_PASS, REDIS_PORT
from redis.asyncio import *  # noqa F403

redis = Redis(  # noqa F405
    host=REDIS_HOST,
    port=REDIS_PORT,
    password=REDIS_PASS,
)
