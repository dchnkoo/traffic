from .session import async_session_manager

from sqlalchemy import exc
import sqlmodel as _sql

from settings import app_settgins

import pydantic as _p
import typing as _t

if _t.TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession
    import uuid


class TableManager[T: _p.BaseModel, _K: (int, "uuid.UUID")]:

    if _t.TYPE_CHECKING:
        id: _K

    type offset = int
    type limit = int

    @staticmethod
    def count_pagination(page: int = 1) -> tuple[offset, limit]:
        offset = (page - 1) * app_settgins.items_per_page
        limit = offset + app_settgins.items_per_page
        return offset, limit

    @classmethod
    @async_session_manager(create=True)
    async def add(
        cls, d: T | dict = None, *, session: _t.Optional["AsyncSession"] = None, **kw
    ) -> _t.Self:
        assert session is not None
        if d is None:
            d = {}
        data = d if isinstance(d, dict) else d.model_dump()
        data = data | kw
        try:
            instance = cls(**data)
            session.add(instance)
            await session.commit()
        except exc.IntegrityError as e:
            await session.rollback()
            raise e
        else:
            return instance

    @async_session_manager(create=True)
    async def save(self, *, session: _t.Optional["AsyncSession"] = None) -> None:
        assert session is not None
        assert self.id is not None, "You cannot save doesn't exist object."

        await session.merge(self)
        await session.commit()
        await self.reload()

    @classmethod
    @async_session_manager
    async def load(
        cls, id: _K, *, session: _t.Optional["AsyncSession"] = None
    ) -> _t.Self:
        assert session is not None
        return await session.get(cls, id)

    @async_session_manager
    async def reload(self, *, session: _t.Optional["AsyncSession"] = None) -> None:
        assert session is not None
        instance = await self.load(self.id)
        self.__dict__.update(instance.__dict__)

    @async_session_manager(create=True)
    async def remove(self, *, session: _t.Optional["AsyncSession"] = None) -> None:
        assert session is not None
        query = _sql.delete(self.__class__).where(self.__class__.id == self.id)
        await session.execute(query)
        await session.commit()

    @classmethod
    @async_session_manager(create=True)
    async def remove_by_id(
        cls, id: _K, *, session: _t.Optional["AsyncSession"] = None
    ) -> None:
        assert session is not None
        query = _sql.delete(cls).where(cls.id == id)
        await session.execute(query)
        await session.commit()

    @async_session_manager
    async def get_relation[
        _R:_sql.Column
    ](
        self,
        relation_table: _R,
        *expr,
        offset: int | None = None,
        limit: int | None = None,
        one: bool = False,
        session: _t.Optional["AsyncSession"] = None,
    ) -> _t.Optional[_R | _t.Sequence[_R]]:
        assert session is not None

        query = _sql.select(relation_table).where(*expr)

        if isinstance(offset, int):
            query = query.offset(offset)
        if isinstance(limit, int):
            query = query.limit(limit)
            
        res = await session.execute(query)
        
        if one:
            return res.scalar_one_or_none()
        else:
            return res.scalars().all()
        
    async def paginate_relation[
        _R:_sql.Column
    ](
        self,
        relation_table: _R,
        *expr,
        page: int = 1
    ) -> _t.Sequence[_R]:
        offset, limit = self.count_pagination(page)
        return await self.get_relation(
            relation_table=relation_table,
            *expr,
            offset=offset,
            limit=limit,
            one=False,
        )

    @async_session_manager
    async def count[
        _R
    ](
        self, relation_table: _R, *expr, query: _t.Any | None = None, session: _t.Optional["AsyncSession"] = None
    ) -> int:
        if query is None:
            query = _sql.select(_sql.func.count()).select_from(relation_table).where(*expr)
        return (await session.execute(query)).scalar_one()

    @async_session_manager
    async def get_random[
        _R:_sql.Column
    ](
        self, table: _R, *expr, session: _t.Optional["AsyncSession"] = None
    ) -> _t.Optional[_R]:
        assert session is not None
        result = await session.execute(
            _sql.select(table).where(*expr).order_by(_sql.func.random()).limit(1)
        )
        return result.scalar_one_or_none()


    @async_session_manager
    async def get_many_to_many[_R:_sql.Column, _M:_sql.Column](
        self, 
        association_table: _M, 
        related_table: _R, 
        join_clause: _t.Sequence, 
        where_clause: _t.Sequence,
        offset: int | None = None,
        limit: int | None = None,
        one: bool = True,
        session: _t.Optional["AsyncSession"] = None
    ):
        query = (
            _sql.select(related_table)
            .join(association_table, *join_clause)
            .where(*where_clause)
        )

        if isinstance(offset, int):
            query = query.offset(offset)

        if isinstance(limit, int):
            query = query.limit(limit)

        result = await session.execute(query)
        if one:
            return result.scalar_one_or_none()
        else:
            return result.scalars().all()

    async def paginate_many_to_many[_R:_sql.Column, _M:_sql.Column](
        self,
        association_table: _M, 
        related_table: _R, 
        join_clause: _t.Sequence, 
        where_clause: _t.Sequence,
        page: int = 1,
    ):
        offset, limit = self.count_pagination(page) 
        return await self.get_many_to_many(
            association_table=association_table,
            related_table=related_table,
            join_clause=join_clause,
            where_clause=where_clause,
            offset=offset,
            limit=limit,
            one=False,
        )
