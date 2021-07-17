from enum import IntEnum


class Permission(IntEnum):
    UNIQUE = -1
    ROOT = 0
    RULER: int = 1
    VIP: int = 2
    USER: int = 4

    def __gt__(self, value: int) -> bool:
        return bool(self.value - value < 1)

    def __str__(self):
        return self.name

    def __repr__(self):
        return '%s (%s)' % (self.name, self.value)
