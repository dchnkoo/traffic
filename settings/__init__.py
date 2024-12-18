from .pathes import APP_DIR, ROOT_DIR
from .additional import Additional
from .database import Postgres
from .redis_conf import Redis
from .trafficbot import Bot


DEFAULT_LANGUAGE = "uk"

postgres = Postgres()

app_settgins = Additional()

bot = Bot()

redis = Redis()
