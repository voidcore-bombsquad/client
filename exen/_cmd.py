from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Callable, List, Any

from argparse import ArgumentParser, ArgumentError
from inspect import isfunction
from dataclasses import dataclass


class Command:

    def __init__(self, name: str, desc: str, keys: List[str], call: Callable):
        self._name = name
        self._desc = desc
        self._keys = keys
        self._call = call
        self._parser: ArgumentParser = ArgumentParser(prog=self.name, 
            description=self.desc, exit_on_error=False)

    def __contains__(self, item: str):
        return item in self.keys or item == self.name

    @property
    def name(self) -> str:
        assert isinstance(self._name, str)
        return self._name[:16]

    @property
    def desc(self) -> str:
        assert isinstance(self._desc, str)
        return self._desc[:32]

    @property
    def keys(self):
        assert isinstance(self._keys, list)
        return self._keys

    @property
    def parser(self) -> Callable:
        assert isinstance(self._parser, ArgumentParser)
        return self._parser

    @property
    def call(self) -> Callable:
        assert isfunction(self._call)
        return self._call

    def execute(self, args: List[str], sender: dataclass) -> Any:
        del sender
        try:
            kwargs = vars(self._parser.parse_args(args))
        except ArgumentError:
            kwargs = {}
        return self._call(**kwargs)