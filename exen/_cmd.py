from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Type, Callable, Any, List

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


class Command(list):
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
        keys: Tuple[str] = None
        """
        self._call = call
        self._name = name if name else call.__name__
        self._desc = desc if desc else call.__doc__
        self._parser: Parser = Parser(prog=self.name, description=self.desc)
        super().__init__(keys if keys else [self.name])

    @property
    def name(self) -> str:
        assert isinstance(self._name, str)
        return self._name[:16]

    @property
    def desc(self) -> str:
        assert isinstance(self._desc, str)
        return self._desc[:32]

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

    def execute(self, sender: dataclass, *args) -> Any:
        """
        Parse args without exception handling
        
        args: Tuple[str]
        sender: dataclass
        """
        kwargs = vars(self._parser.parse_args(args))
        for k, v in vars(sender).items():
            if k in kwargs and kwargs[k] is self.empty:
                kwargs[k] = v
        return self.call(**kwargs)     
