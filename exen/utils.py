from __future__ import annotations
from typing import TYPE_CHECKING

from tempfile import TemporaryDirectory
from os.path import isfile, isdir
from hashlib import md5

import json
import os


if TYPE_CHECKING:
    from typing import Callable, List, Dict, Any
    Json = Dict[str, Any]


def exists(path: str) -> bool:
    try:
        return os.path.exists(path)
    except PermissionError:
        pass
    except SyntaxError:
        pass


def readfile(path: str) -> str:
    if (exists(path) and
            isfile(path) and os.access(path, os.R_OK)):
        with open(path, 'r') as file:
            contents = file.read()
            file.close()
        return contents
    return ''


def readjson(path: str) -> Json:
    try:
        return json.loads(readfile(path))
    except json.JSONDecodeError:
        return {}


def makedir(path: str) -> bool:
    try:
        os.makedirs(path, exist_ok=True)
        with TemporaryDirectory(dir=path):
            return True
    except OSError:
        return False


def listdir(path: str) -> List[str]:
    if exists(path):
        if isdir(path) and os.access(path, os.R_OK):
            return os.listdir(path)
    else:
        makedir(path)
    return []


def md5sum(path: str) -> str:
    if exists(path) and os.path.isfile(path) and os.access(path, os.R_OK):
        result = md5()
        with open(path, 'rb') as f:
            while True:
                chunk = f.read(2 ** 20)
                if not chunk:
                    break
                result.update(chunk)
        return result.hexdigest()
    raise ValueError(path)


def redefine(new: Callable) -> Callable:
    if len(new.__bases__) != 1:
        raise ValueError()
    base = new.__bases__[0]
    module = __import__(base.__module__, fromlist=[''])
    setattr(module, base.__name__, new)

    def decorator() -> Callable:
        return new
    return decorator