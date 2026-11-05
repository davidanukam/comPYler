from dataclasses import dataclass

from tokenization import Token

@dataclass
class NodeExpr:
    int_lit: Token


@dataclass
class NodeExit:
    expr: "NodeExpr"
