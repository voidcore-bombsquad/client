from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Optional

from ._plugin import KeyPlugin

import logging
import os
import ba


class Log(KeyPlugin):
    """
    Provides logging feature for chat commands
    """

    def __init__(self, path: str = None):
        """
        path: str = None
        """
        super().__init__('Enable Cmds')
        self._logger: Optional[logging.Logger] = None
        self._formatter: Optional[logging.Formatter] = None
        self._handler: Optional[logging.FileHandler] = None
        if path:
            self._path = path
        else:
            self._path = ba.app.config.get('Log Path', 'temp.log')

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
