from dataclasses import dataclass
from lib import ast
from typing import Iterable, Dict, Any


@dataclass
class Callable:
    name: str
    body: ast.Block
    params: Iterable[ast.Param]


@dataclass
class Class:
    name: str
    body: Iterable[Callable]


@dataclass
class Instance:
    parent: Class
    data: Dict[str, Any]
