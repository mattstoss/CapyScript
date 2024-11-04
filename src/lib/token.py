from dataclasses import dataclass
from enum import Enum, auto


class TokenKind(Enum):
    Print = auto()
    Identifier = auto()
    StringLiteral = auto()
    Func = auto()
    OpenParen = auto()
    CloseParen = auto()
    OpenBracket = auto()
    CloseBracket = auto()
    Equal = auto()
    Let = auto()
    Comma = auto()
    Return = auto()
    Dot = auto()
    Class = auto()


@dataclass
class Token:
    kind: TokenKind
    string: str
