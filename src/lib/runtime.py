from dataclasses import dataclass
from lib import ast
from typing import Iterable


@dataclass
class Callable:
    name: str
    body: ast.Block
    params: Iterable[ast.Param]
