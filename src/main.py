import sys
import subprocess

from macros import *

from tokenization import Tokenizer, Token, TokenType


class Compyler:
    def __init__(self):
        self.main()

    def tokenize(self, string: str) -> list[Token]:
        tokens: list[Token] = []

        char_buf: list[str] = []

        i = 0
        while True:
            if i >= len(string):
                return tokens

            char = string[i]

            # Add first character IF it is a letter (can't start a line with a number)
            if char.isalpha():
                char_buf.append(string[i])
                i += 1

                # Add the rest of the letters
                while string[i].isalnum():
                    char_buf.append(string[i])
                    i += 1

                if "".join(char_buf) == "exit":
                    tokens.append(Token(type=TokenType.exit, value=None))
                    char_buf.clear()
                    continue
                else:
                    print("[Error]: You messed up!")
                    return EXIT_FAILURE

            elif string[i].isdigit():
                char_buf.append(string[i])
                i += 1

                # Add the rest of the numbers
                while string[i].isdigit():
                    char_buf.append(string[i])
                    i += 1

                tokens.append(Token(type=TokenType.int_lit, value="".join(char_buf)))
                char_buf.clear()

            elif string[i] == ";":
                tokens.append(Token(type=TokenType.semi, value=None))
                char_buf.clear()
                i += 1

            elif string[i].isspace():
                i += 1
                continue

            else:
                print("[Error]: You messed up!")
                return EXIT_FAILURE

    def tokens_to_asm(self, tokens: list[Token]) -> str:
        output = (
            f"bits 64\n\ndefault rel\nextern ExitProcess\n\nglobal _start:\n\n_start:\n"
        )

        for i in range(len(tokens)):
            if tokens[i].type == TokenType.exit:
                if (i + 1 < len(tokens)) and tokens[i + 1].type == TokenType.int_lit:
                    if (i + 2 < len(tokens)) and tokens[i + 2].type == TokenType.semi:
                        # output += f"    mov rax, 60\n"
                        # output += f"    mov rdi, {tokens[i + 1].value}\n"
                        # output += f"    syscall"
                        output += f"    sub rsp, 40\n"
                        output += f"    xor rcx, rcx\n"
                        output += f"    call ExitProcess"

        return output

    def main(self) -> int:
        argc = len(sys.argv)
        argv = sys.argv

        if argc != 2:
            print("Incorrect usage. Correct usage is...")
            print("python src/main.py <input.wxt>")
            return EXIT_FAILURE

        contents: list[str] = []
        with open(rf"{argv[1]}", "r", encoding="utf-8") as f:
            for char in f.readline():
                contents.append(char)

        src: str = "".join(contents)

        tokenizer = Tokenizer(src)

        tokens = tokenizer.tokenize()

        output = self.tokens_to_asm(tokens)

        # write output to .asm file
        with open("test.asm", "w") as f:
            lines = output.split("\n")
            for line in lines:
                f.write(line + "\n")

        subprocess.run(["nasm", "-f", "win64", "test.asm", "-o", "test.obj"])
        subprocess.run(
            ["ld", "-m", "i386pep", "-o", "test.exe", "test.obj", "-lkernel32"]
        )
        subprocess.run(["./test.exe"])

        return EXIT_SUCCESS


if __name__ == "__main__":
    Compyler()
