from pydantic_settings import BaseSettings
from .settings_conf import config

import pydantic as _p

import datetime as _date

import typing as _t


class Redis(BaseSettings):
    model_config = config
    key = "redis"

    host: str = _p.Field("localhost", alias=key + "_host")
    port: int = _p.Field(6379, alias=key + "_port")
    db: int = _p.Field(0, alias=key + "_db")
    password: str = _p.Field("", alias=key + "_password")
    username: str = _p.Field("", alias=key + "_user")

    @property
    def default_cache_live_time(self):
        return (
            ((now := _date.datetime.now(_date.timezone.utc)) + _date.timedelta(hours=5))
            - now
        ).seconds

    def dsn(self, db: _t.Optional[int] = None):
        return self.key + f"://{self.username}:{self.password}@{self.host}:{self.port}/{db or self.db}"
    