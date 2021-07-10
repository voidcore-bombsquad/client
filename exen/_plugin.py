import ba


class KeyPlugin(ba.Plugin):
    def __init__(self, key: str = None):
        if not key:
            key = 'Enable {}'.format(self.__name__)
        self._key = key

    @property
    def key(self) -> str:
        assert isinstance(self._key, str)
        return self._key

    def __getattribute__(self, name: str):
        if name in ['on_app_launch', 'on_app_shutdown']:
            if ba.app.config.get(self.key, True):
                return getattr(self, name)
        return getattr(super(), name)
