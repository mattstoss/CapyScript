from dataclasses import dataclass
from typing import Iterable


class Node:
    pass


class StmtNode:
    pass


class ExprNode:
    pass


@dataclass
class Print(StmtNode):
    expr: ExprNode


@dataclass
class Return(StmtNode):
    expr: ExprNode


@dataclass
class VarDecl(StmtNode):
    name: str
    expr: ExprNode


@dataclass
class Param(StmtNode):
    name: str


@dataclass
class Arg(StmtNode):
    expr: ExprNode


@dataclass
class Block(StmtNode):
    nodes: Iterable[Node]


@dataclass
class FuncDecl(StmtNode):
    name: str
    params: Iterable[Param]
    body: Block


@dataclass
class ClassDecl(StmtNode):
    name: str
    body: Iterable[FuncDecl]


@dataclass
class String(ExprNode):
    value: str


@dataclass
class Identifier(ExprNode):
    value: str


@dataclass
class Assignment(ExprNode):
    name: str
    expr: ExprNode


@dataclass
class Call(ExprNode):
    value: ExprNode
    args: Iterable[Arg]


@dataclass
class GetProperty(ExprNode):
    instance: ExprNode
    property: str
