import sys
import subprocess

from macros import *

from tokenization import Tokenizer, Token, TokenType


class Compyler:
    def __init__(self):
        self.main()

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
