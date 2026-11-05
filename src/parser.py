from macros import *

from tokenization import Token, TokenType

from nodes import NodeExpr, NodeExit


class Parser:
    def __init__(self, tokens: list[str]):
        self.tokens: list[str] = tokens
        self.curr_dex: int = 0

    def peak(self, ahead: int = 1) -> Token | None:
        if self.curr_dex + ahead >= len(self.tokens):
            return None
        else:
            return self.tokens[self.curr_dex]

    def consume(self) -> Token:
        char: str = self.tokens[self.curr_dex]
        self.curr_dex += 1
        return char

    def parse_expr(self) -> NodeExpr:
        if self.peak() and self.peak().type == TokenType.int_lit:
            return NodeExpr(int_lit=self.consume())
        else:
            return None

    def parse(self) -> NodeExit | None:
        exit_node: NodeExit | None = None

        while self.peak():
            if self.peak().type == TokenType.exit:
                self.consume()

                if node_expr := self.parse_expr():
                    exit_node = NodeExit(expr=node_expr)
                else:
                    print("[Error]: Invalid Expression")
                    return EXIT_FAILURE

                if self.peak() or self.peak().type != TokenType.semi:
                    print("[Error]: Invalid Expression")
                    return EXIT_FAILURE

        self.curr_dex = 0
        return exit_node
