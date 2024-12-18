from pydantic_settings import BaseSettings
from .settings_conf import config

import pydantic as _p


class Bot(BaseSettings):
    model_config = config

    token: str = _p.Field(..., alias="bot_token")
    