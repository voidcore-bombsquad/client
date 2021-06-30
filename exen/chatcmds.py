from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ._me import ArgumentParser

from ._chatcmd import ChatCommand
from ._chatcmds import register_chatcmd
from _ba import chatmessage

command = ChatCommand(name='test', desc='desc', keys=['test', 'test2'])


@command.call
def test(client_id: int):
    chatmessage(message=str(client_id))


@command.parser
def test(parser: ArgumentParser):
    parser.add_argument('-c', '--client_id', type=int)


register_chatcmd(command)