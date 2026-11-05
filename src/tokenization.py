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
        self.curr_idex: str = 0

    def peak(self) -> str | None:
        if self.curr_idex + 1 >= len(self.src):
            return None
        else:
            return self.src[self.curr_idex]

    def tokenize(self) -> list[Token]:
        tokens: list[Token] = []

        char_buf: list[str] = []

        i = 0
        while True:
            if i >= len(self.src):
                return tokens

            char = self.src[i]

            # Add first character IF it is a letter (can't start a line with a number)
            if char.isalpha():
                char_buf.append(self.src[i])
                i += 1

                # Add the rest of the letters
                while self.src[i].isalnum():
                    char_buf.append(self.src[i])
                    i += 1

                if "".join(char_buf) == "exit":
                    tokens.append(Token(type=TokenType.exit, value=None))
                    char_buf.clear()
                    continue
                else:
                    print("[Error]: You messed up!")
                    return EXIT_FAILURE

            elif self.src[i].isdigit():
                char_buf.append(self.src[i])
                i += 1

                # Add the rest of the numbers
                while self.src[i].isdigit():
                    char_buf.append(self.src[i])
                    i += 1

                tokens.append(Token(type=TokenType.int_lit, value="".join(char_buf)))
                char_buf.clear()

            elif self.src[i] == ";":
                tokens.append(Token(type=TokenType.semi, value=None))
                char_buf.clear()
                i += 1

            elif self.src[i].isspace():
                i += 1
                continue

            else:
                print("[Error]: You messed up!")
                return EXIT_FAILURE
