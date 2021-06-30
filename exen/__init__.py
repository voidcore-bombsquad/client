from ._chatcmds import ChatCommands

import ba


cmds: ChatCommands


class ExtensionsEngine(ba.Plugin):
    cmds: ChatCommands = ChatCommands()

    __dict__ = {'cmds': cmds}

    def __getattribute__(self, item: str):
        if item in ['on_app_launch', 'on_app_pause', 'on_app_continue', 'on_app_shutdown']:
            for n, v in vars(self).items():
                if isinstance(v, ba.Plugin):
                    if ba.app.config.get('Enable %s' % n.title(), True):
                        try:
                            getattr(v, item)()
                        except Exception as e:
                            ba.print_exception(e)
                globals().setdefault(n, v)
        return super().__getattribute__(item)