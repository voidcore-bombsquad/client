from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import List, Optional, Union


from ._sqlbase import SQLBase
from ._logging import Log
from ._sender import Sender
from ._cmd import Command

import weakref
import ba


class ChatCommands(list, ba.Plugin):

    def __init__(self):
        super(list, self).__init__()
        self._sqlbase: SQLBase = SQLBase('test.db')
        self._log: Log = Log('test.log')

    @property
    def sqlbase(self) -> SQLBase:
        assert isinstance(self._sqlbase, SQLBase)
        return weakref.ref(self._sqlbase)()

    @property
    def log(self) -> Log:
        assert isinstance(self._log, Log)
        return weakref.ref(self._log)()

    def __getitem__(self, item: str) -> ChatCommand:
        if isinstance(item, str):
            for chatcmd in self:
                if item in chatcmd:
                    return chatcmd
        return super().__getitem__(item)

    def on_chat_message(self, message: str, client_id: int) -> None:
        del client_id
        return message


class ChatCommand(Command):

    def execute(self, args: List[str], client_id: int) -> Optional[Union[ba.Lstr, str]]:
        try:
            return super().execute(args, Sender(client_id=client_id))
        except TypeError:
            return ba.Lstr(translate=('command.invalidOutput', 'invalid output'))
        except Exception as e:
            return ba.Lstr(translate=('commandErrorMessage', 'error while running: ${ERROR}'),
                        subs=[('${ERROR}', str(e))])

    __call__ = execute


def register_chatcmd(chatcmd: ChatCommand):
    from exen import cmds 

    if chatcmd in cmds:
        raise ValueError(chatcmd)
    cmds[chatcmd.name] = chatcmd
