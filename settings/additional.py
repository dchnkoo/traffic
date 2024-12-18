from pydantic_settings import BaseSettings
from .settings_conf import config


class Additional(BaseSettings):
    model_config = config

    items_per_page: int = 10
