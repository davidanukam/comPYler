from macros import *

from enum import Enum, auto
from typing import Optional

from dataclasses import dataclass


class TokenType(Enum):
    exit = auto()
    int_lit = auto()
    semi = auto()


@dataclass
class Token:
    type: TokenType
    value: Optional[str] | None = None


class Tokenizer:
    def __init__(self, src: str):
        self.src: str = src
        self.curr_dex: int = 0

    def peak(self, ahead: int = 1) -> str | None:
        if self.curr_dex + ahead >= len(self.src):
            return None
        else:
            return self.src[self.curr_dex]

    def consume(self) -> str:
        char: str = self.src[self.curr_dex]
        self.curr_dex += 1
        return char

    def tokenize(self) -> list[Token]:
        tokens: list[Token] = []

        char_buf: list[str] = []

        # Add first character IF it is a letter (can't start a line with a number)
        while self.peak():
            if self.peak().isalpha():
                char_buf.append(self.consume())

                # Add the rest of the letters
                while self.peak() and self.peak().isalnum():
                    char_buf.append(self.consume())

                if "".join(char_buf) == "exit":
                    tokens.append(Token(type=TokenType.exit, value=None))
                    char_buf.clear()
                else:
                    print("[Error]: You messed up!")
                    return EXIT_FAILURE

            elif self.peak().isdigit():
                char_buf.append(self.consume())

                # Add the rest of the numbers
                while self.peak() and self.peak().isdigit():
                    char_buf.append(self.consume())

                tokens.append(Token(type=TokenType.int_lit, value="".join(char_buf)))
                char_buf.clear()

            elif self.peak() == ";":
                self.consume()
                tokens.append(Token(type=TokenType.semi, value=None))
                char_buf.clear()

            elif self.peak().isspace():
                self.consume()

            else:
                print("[Error]: You messed up!")
                return EXIT_FAILURE

        self.curr_dex = 0
        return tokens
