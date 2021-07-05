from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import List, Optional, Union


from ._sqlbase import SQLBase
from ._logging import Log

from ._cmd import Command
from ._sender import Sender

import ba


class ChatCommands(dict, ba.Plugin):

    def __init__(self):
        super(dict, self).__init__()
        self._sqlbase: SQLBase = SQLBase()
        self._log: Log = Log()

    @property
    def sqlbase(self) -> SQLBase:
        assert isinstance(self._sqlbase, SQLBase)
        return self._sqlbase

    @property
    def log(self) -> Log:
        assert isinstance(self._log, Log)
        return self._log
    
    @classmethod
    def register(cls, chatcmd: ChatCommand) -> None:
        if chatcmd.name in ba.app.cmds:
            raise ValueError(chatcmd.name)
        ba.app.cmds[chatcmd.name] = chatcmd

    def on_chat_message(self, message: str, client_id: int) -> None:
        del client_id
        return message

    def on_app_launch(self) -> None:
        self.log.on_app_launch()
        self.sqlbase.on_app_launch()

    def on_app_shutdown(self) -> None:
        self.log.on_app_shutdown()
        self.sqlbase.on_app_shutdown()


class ChatCommand(Command):

    @staticmethod
    def makesender(client_id: int) -> Sender:
        from _ba import get_game_roster

        kwargs = {'client_id': client_id}
        for client in get_game_roster():
            if client['client_id'] == client_id:
                kwargs['account_id'] = client['account_id']
        # TODO: unique_code, permissions from sqlbase
        return Sender(**kwargs)

    def execute(self, args: List[str], client_id: int) -> Optional[Union[ba.Lstr, str]]:
        try:
            sender = self.makesender(client_id=client_id)
            return super().execute(args, sender)
        except TypeError:
            return ba.Lstr(translate=('command.invalidOutput', 'invalid output'))
        except Exception as e:
            return ba.Lstr(translate=('commandErrorMessage', 'error while running: ${ERROR}'),
                        subs=[('${ERROR}', str(e))])

    __call__ = execute
