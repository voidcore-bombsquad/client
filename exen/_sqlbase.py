from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Optional

import sqlite3


class SQLBase:
    """
    Subsystem plugin of Extensions Engine
    Typically used with chat commands
    """
    
    def __init__(self, path: str):
        """
        path: str
        """
        self._conn: Optional[sqlite3.Connection] = None
        self._cursor: Optional[sqlite3.Cursor] = None
        self._path = path

    def __call__(self, *args, **kwargs) -> bool:
        """
        Execute sql-string in sqlite3.Cursor

        *args
        **kwargs
        """
        try:
            self.cursor.execute(*args, **kwargs)
            return True
        except sqlite3.OperationalError as e:
            from ba import print_exception

            print_exception(e)

    def __getitem__(self, item: int):
        """
        Fetch items from sqlite3.Cursor and returns
        specific item

        item: int
        """
        return self.cursor.fetchall()[item]

    def _sqlbase_init_(self) -> None:
        """
        Initializates 'default' sqlbase for chat commands
        """
        self('CREATE TABLE IF NOT EXISTS permissions ('
            'account_id TEXT NOT NULL PRIMARY KEY,'   
            'unique_code TEXT DEFAULT VIP,'
            'level INTEGER DEFAULT 1,'
            'expire_in TEXT)')
        self('CREATE TABLE IF NOT EXISTS intruders ('
            'account_id TEXT NOT NULL PRIMARY KEY,'
            'punishment INTEGER DEFAULT 1,'
            'comment TEXT'
            'expire_in TEXT)')
        self._conn.commit()

    @property
    def cursor(self) -> sqlite3.Cursor:
        assert isinstance(self._cursor, sqlite3.Cursor)
        return self._cursor

    @property
    def path(self) -> str:
        assert isinstance(self._path, str)
        return self._path

    def on_app_launch(self) -> None:
        self._conn = sqlite3.connect(self.path)
        self._cursor = self._conn.cursor()
        self._sqlbase_init_()

    def on_app_shutdown(self) -> None:
        self._conn.commit()
        self._cursor.close()
        self._conn.close()
