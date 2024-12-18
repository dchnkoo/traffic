import pydantic.dataclasses as dataclasses
from pydantic import ConfigDict

from aiogram.utils.markdown import markdown_decoration
import aiogram.types as aiogram_types

from settings import DEFAULT_LANGUAGE

from utils.chat import ChatModel

from traffic.bot import trafficbot


class BaseModel:

    @staticmethod
    def markdown_string(string: str):
        return markdown_decoration.quote(string)


class TelegramUserModel(BaseModel, ChatModel, aiogram_types.User):
    model_config = ConfigDict(
        use_enum_values=True,
        extra="ignore",
        validate_assignment=True,
        populate_by_name=True,
        arbitrary_types_allowed=True,
        defer_build=True,
    )

    selected_language: str | None = None
    blocked: bool = False

    @property
    def chat_id(self):
        return self.id
    
    @property
    def bot(self):
        return trafficbot

    @property
    def language(self):
        if self.selected_language is None:
            return DEFAULT_LANGUAGE
        return self.selected_language

    @property
    def premium(self):
        return bool(self.is_premium)
    
    @property
    def escaped_first_name(self):
        return self.markdown_string(self.first_name)

    @property
    def escaped_last_name(self):
        if self.last_name:
            return self.markdown_string(self.last_name)

    @property
    def escaped_full_name(self):
        if self.last_name:
            return f"{self.escaped_first_name} {self.escaped_last_name}"
        return self.escaped_first_name
    

@dataclasses.dataclass(kw_only=True, validate_on_init=True)
class TopicModel(BaseModel):
    name: str

    @property
    def escaped_name(self):
        return self.markdown_string(self.name)


@dataclasses.dataclass(kw_only=True, validate_on_init=True)
class OfferModel(BaseModel):
    name: str
    ordered_traffic: int
    payment: float
    comment: str | None = None
    taboo: str
    completed: bool = False

    @property
    def escaped_name(self):
        return self.markdown_string(self.name)
    
    @property
    def escaped_comment(self):
        return self.markdown_string(self.comment)
    
    @property
    def escaped_taboo(self):
        return self.markdown_string(self.taboo)


@dataclasses.dataclass(kw_only=True, validate_on_init=True)
class UserInfoModel:
    balance: float = 0
    current_withdraw_sum: int = 0
    already_withdrawed_sum: int = 0
    earned_from_partners: int = 0


@dataclasses.dataclass(kw_only=True, validate_on_init=True)
class TeamModel:
    name: str
    description: str
