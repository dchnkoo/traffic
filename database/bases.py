from datetime import datetime

from .funcs import funcs

import sqlmodel as _sql

import uuid


class BaseId:
    id: int = _sql.Field(primary_key=True)


class BaseUUID:
    id: uuid.UUID = _sql.Field(default_factory=uuid.uuid4, primary_key=True)


class BaseCreateDate:
    created: datetime = _sql.Field(
        sa_type=_sql.DateTime(timezone=True), default_factory=funcs.now_utc
    )

    @property
    def time_passed_from_created(self):
        return (funcs.now_utc() - self.created) 

    @property
    def time_passed_from_created_minutes(self):
        return self.time_passed_from_created.seconds // 60
    
    @property
    def time_passed_from_created_hours(self):
        return self.time_passed_from_created_minutes // 60


class BaseUpdatedDate:
    updated: datetime | None = _sql.Field(
        sa_type=_sql.DateTime(timezone=True),
        sa_column_kwargs={"onupdate": funcs.now_utc},
        default=None,
    )

    @property
    def time_passed_from_updated(self):
        if (date := self.updated) is None:
            return
        return (funcs.now_utc() - date) 

    @property
    def time_passed_from_updated_minutes(self):
        time = self.time_passed_from_updated
        if time is None:
            return
        return time.seconds // 60
    
    @property
    def time_passed_from_updated_hours(self):
        time = self.time_passed_from_updated_minutes
        if time is None:
            return
        return time // 60


class BaseDates(BaseCreateDate, BaseUpdatedDate):
    ...
