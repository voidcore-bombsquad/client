from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Optional

from ._enums import Permissions
from dataclasses import dataclass


@dataclass
class Sender:
    client_id: int = 0
    account_id: Optional[str] = ''
    level: int = Permissions.USER
    unique_code: str = 'USER'

    def __repr__(self) -> str:
        return 'Sender(%s)' % ', '.join(
            ['%s=%s' % i for i in vars(self).items()])


def makesender(client_id: int) -> Sender:
    from _ba import get_game_roster

    kwargs = {'client_id': client_id}
    for c in get_game_roster():
        if c['client_id'] == client_id:
            kwargs['account_id'] = c['account_id']
            break
    return Sender(**kwargs)