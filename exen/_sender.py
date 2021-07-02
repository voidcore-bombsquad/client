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
    unique_code: str = str(level)

    def __repr__(self):
        return 'Sender(%s)' % ', '.join(
            ['%s=%s' % i for i in vars(self).items()])
