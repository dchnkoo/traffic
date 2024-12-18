from datetime import datetime, timezone


class DBFuncs:

    @property
    def now_utc(self):
        return lambda: datetime.now(timezone.utc)


funcs = DBFuncs()
