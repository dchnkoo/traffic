from aiogram.fsm.storage.redis import RedisStorage
from aiogram import Bot, Dispatcher

from settings import redis, bot


trafficbot = Bot(bot.token)
storage = RedisStorage.from_url(
    redis.dsn(),
    state_ttl=redis.default_cache_live_time,
    data_ttl=redis.default_cache_live_time,
)
dp = Dispatcher(storage=storage)
