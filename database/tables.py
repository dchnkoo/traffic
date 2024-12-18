from .manager import TableManager
from .models import *
from .bases import *

from exc import UserBlocked

import sqlmodel as _sql
import typing as _t
import inspect


metadata = _sql.SQLModel


type total = int

type completed = total

type uncompleted = completed


class TelegramUser(
    metadata, TelegramUserModel, TableManager[TelegramUserModel | aiogram_types.User, int], BaseDates, table=True
):
    
    id: int = _sql.Field(
        primary_key=True, sa_type=_sql.BigInteger, index=True
    )

    async def count_offers(self, completed: bool | None = None):
        if completed is not None:
            stmt = (
                _sql.select(_sql.func.count(Offer.id))
                .join(UserOffers, Offer.id == UserOffers.offer_id)
                .where(
                    UserOffers.user_id == self.id,
                    Offer.completed.is_(completed)
                )
            )

        match completed:
            case None:
                return await self.count(UserOffers, UserOffers.user_id == self.id)
            case _:
                return await self.count(..., query=stmt)

    async def offers_info(self) -> tuple[total, completed, uncompleted]:
        total = await self.count_offers()
        completed = await self.count_offers(completed=True)
        uncompleted = await self.count_offers(completed=False)
        return (total, completed, uncompleted)

    async def count_traffic(self):
        return await self.count(UserTraffic, UserTraffic.user_id == self.id)

    async def count_traffic_by_offer(self, offer_id: int):
        return await self.count(UserTraffic, UserTraffic.user_id == self.id, UserTraffic.offer_id == offer_id)
    
    async def count_partners(self):
        return await self.count(UserPartners, UserPartners.user_id == self.id)

    async def is_admin(self):
        admin = await self.get_relation(Admins, Admins.user_id == self.id, one=True)
        return bool(admin)

    async def set_admin(self):
        await Admins.add(user_id=self.id)

    async def unset_admin(self):
        await Admins.remove_by_id(self.id)

    async def get_offers(self, page: int = 1):
        return self.paginate_many_to_many(
            UserOffers,
            Offer,
            UserOffers.offer_id == Offer.id,
            UserOffers.user_id == self.id,
            page=page,
        )
    
    async def get_offer(self, offer_id: int) -> _t.Optional["Offer"]:
        return await self.get_many_to_many(
            UserOffers,
            Offer,
            UserOffers.offer_id == offer_id,
            UserOffers.user_id == self.id,
        )
    
    async def get_offer_links(self, offer_id: int, page: int = 1) -> _t.Sequence["OfferLink"]:
        return await self.paginate_relation(
            OfferLink,
            OfferLink.user_id == self.id,
            OfferLink.offer_id == offer_id,
            page=page,
        )
    
    async def get_team(self) -> _t.Optional["Team"]:
        return await self.get_many_to_many(
            TeamMembers,
            Team,
            TeamMembers.team_id == Team.id,
            TeamMembers.user_id == self.id,
            one=True,
        )

    def __getattribute__(self, name):
        attr = object.__getattribute__(self, name)
        if name != (field := "blocked"):
            if (
                callable(attr) 
                and inspect.iscoroutinefunction(attr) 
                and object.__getattribute__(self, field)
            ):
                raise UserBlocked()
        return attr


user_foregin_key = _sql.Field(foreign_key="telegramuser.id", ondelete="CASCADE")


class Topic(metadata, TopicModel, TableManager[TopicModel, int], BaseId, BaseDates, table=True):
    name: str = _sql.Field(unique=True)

    async def count_offers(self, completed: bool | None = None):
        if completed is not None:
            stmt = (
                _sql.select(_sql.func.count(Offer.id))
                .join(OfferTopics, Offer.id == OfferTopics.offer_id)
                .where(
                    OfferTopics.topic_id == self.id, 
                    Offer.completed.is_(completed)
                )
            )

        match completed:
            case None:
                return await self.count(OfferTopics, OfferTopics.topic_id == self.id)
            case _:
                return await self.count(..., query=stmt)
            
    async def count_uncompletd_offers(self) -> int:
        return await self.count_offers(completed=False)
    
    async def get_offers(self, page: int = 1):
        return await self.paginate_many_to_many(
            OfferTopics,
            Offer,
            OfferTopics.offer_id == Offer.id,
            OfferTopics.topic_id == self.id,
            page=page,
        )


topic_foregin_key = _sql.Field(foreign_key="topic.id", ondelete="CASCADE")


class Offer(metadata, OfferModel, TableManager[OfferModel, int], BaseId, BaseDates, table=True):
    
    async def count_traffers(self) -> int:
        return await self.count(UserOffers, UserOffers.offer_id == self.id)
    
    async def get_topics(self) -> _t.Sequence[Topic]:
        return await self.get_many_to_many(
            OfferTopics,
            Topic,
            OfferTopics.topic_id == Topic.id,
            OfferTopics.offer_id == self.id
        )
    
    async def get_traffers(self, page: int = 1) -> _t.Sequence[TelegramUser]:
        return await self.paginate_many_to_many(
            UserOffers,
            TelegramUser,
            UserOffers.user_id == TelegramUser.id,
            UserOffers.offer_id == self.id,
            page=page
        )
    
    async def get_links(self, page: int = 1) -> _t.Sequence["OfferLink"]:
        return await self.paginate_relation(
            OfferLink,
            OfferLink.offer_id == self.id,
            page=page,
        )


offer_foregin_key = _sql.Field(foreign_key="offer.id", ondelete="CASCADE")


class UserOffers(metadata, TableManager["UserOffers", int], BaseId, BaseDates, BaseCreateDate, table=True):
    
    user_id: int = user_foregin_key
    offer_id: int = offer_foregin_key


class OfferLink(metadata, TableManager["OfferLink", int], BaseId, BaseCreateDate, table=True):

    offer_id: int = offer_foregin_key
    user_id: int = user_foregin_key
    link: str


class OfferTopics(metadata, TableManager["OfferTopics", int], BaseId, BaseCreateDate, table=True):

    offer_id: int = offer_foregin_key
    topic_id: int = topic_foregin_key


class Admins(metadata, TableManager["Admins", int], BaseId, BaseCreateDate, table=True):

    user_id: int = user_foregin_key


class UserTraffic(metadata, TableManager["UserTraffic", int], BaseId, BaseCreateDate, table=True):
    
    user_id: int = user_foregin_key
    traffic_user_id: int = user_foregin_key
    offer_id: int = offer_foregin_key


class UserPartners(metadata, TableManager["UserPartners", int], BaseId, BaseCreateDate, table=True):

    user_id: int = user_foregin_key
    partner_id: int = user_foregin_key


class UserInfo(metadata, BaseId, UserInfoModel, TableManager[UserInfoModel, int], table=True):
    level_id: _t.Optional[int] = _sql.Field(foreign_key="level.id", ondelete="SET NULL")


class Level(metadata, TableManager["Level", int], BaseId, BaseCreateDate, table=True):
    name: str = _sql.Field(unique=True)
    percent: int = _sql.Field(default=0, ge=0, le=100)


class Team(metadata, BaseId, TeamModel, BaseDates, TableManager[TeamModel, int], table=True):
    name: str = _sql.Field(unique=True)
    creator_id: int = user_foregin_key

    async def get_members(self, page: int = 1) -> _t.Sequence[TelegramUser]:
        return await self.paginate_many_to_many(
            TeamMembers,
            TelegramUser,
            TeamMembers.user_id == TelegramUser.id,
            TeamMembers.team_id == self.id,
            page=page,
        )
    
    async def get_team_topics(self) -> _t.Sequence[Topic]:
        return await self.get_many_to_many(
            TeamTopics,
            Topic,
            TeamTopics.topic_id == Topic.id,
            TeamTopics.team_id == self.id,
        )
    
    async def get_creator(self):
        return await TelegramUser.load(self.creator_id)


team_foregin_key = _sql.Field(foreign_key="team.id", ondelete="CASCADE")


class TeamTopics(metadata, TableManager["TeamTopics", int], BaseId, BaseCreateDate, table=True):
    team_id: int = team_foregin_key
    topic_id: int = topic_foregin_key


class TeamMembers(metadata, TableManager["TeamMembers", int], BaseId, BaseCreateDate, table=True):
    user_id: int = user_foregin_key
    team_id: int = team_foregin_key
