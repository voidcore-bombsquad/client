from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Optional

import logging
import os


class Log:
    """
    Provides logging feature
    """

    def __init__(self, path: str):
        """
        path: str
        """
        self._logger: Optional[logging.Logger] = None
        self._formatter: Optional[logging.Formatter] = None
        self._handler: Optional[logging.FileHandler] = None
        self._path = path

    def __getattr__(self, item: str):
        """
        Returns selected attribute of Log.logger

        item: str
        """
        return getattr(self.logger, item)

    @property
    def logger(self) -> logging.Logger:
        assert isinstance(self._logger, logging.Logger)
        return self._logger

    @property
    def path(self) -> str:
        assert isinstance(self._path, str)
        return self._path

    def on_app_launch(self) -> None:
        self._logger = logging.Logger(os.path.basename(self.path))
        self._formatter = logging.Formatter(
            '[%(levelname)s] %(asctime)s: %(message)s')
        self._handler = logging.FileHandler(self.path)
        self._handler.setFormatter(self._formatter)
        self._handler.setLevel(logging.INFO)
        self._logger.addHandler(self._handler)
        self.info('on_app_launch')

    def on_app_shutdown(self) -> None:
        self.info('on_app_shutdown')
