from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Type, Callable, List

from argparse import ArgumentParser, ArgumentError
from dataclasses import dataclass
from inspect import isfunction


__all__ = ['Command']


class _empty:
    pass


class Parser(ArgumentParser):
    # TODO: wait for Python 3.9
    def error(self, message: str) -> None:
        raise ArgumentError(message)


class Command:
    """Parent class of ChatCommands"""

    def __init__(self,
          call: Callable,
          name: str = None, 
          desc: str = None, 
          keys: List[str] = None):
        """
        call: Callable 
        name: str = None
        desc: str = None
        keys: List[str] = None
        """
        self._call = call
        self._name = (name if name else call.__name__)[:16]
        self._desc = (desc if desc else call.__doc__)[:32]
        self._keys = keys if keys else [self.name]
        self._parser: Parser = Parser(prog=self.name, description=self.desc)

    def __call__(self, args: List[str], sender: dataclass):
        """
        Parse args

        args: List[str]
        sender: dataclass
        """
        try:
            kwargs = vars(self._parser.parse_args(args))
            for k, v in vars(sender).items():
                if k in kwargs and kwargs[k] is self.empty:
                    kwargs[k] = v
            return self.call(**kwargs)
        except ArgumentError:
            return None

    @property
    def name(self) -> str:
        assert isinstance(self._name, str)
        return self._name

    @property
    def desc(self) -> str:
        assert isinstance(self._desc, str)
        return self._desc

    @property
    def keys(self) -> List[str]:
        assert isinstance(self._keys, list)
        return self._keys

    @property
    def parser(self) -> Callable:
        assert isinstance(self._parser, Parser)
        return self._parser

    @property
    def call(self) -> Callable:
        assert isfunction(self._call)
        return self._call
    
    @property
    def empty(self) -> Type[_empty]:
        return _empty
