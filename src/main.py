import sys
import subprocess

from macros import *

from tokenization import Tokenizer
from parser import Parser
from generation import Generator


class Compyler:
    def __init__(self):
        self.main()

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

        parser = Parser(tokens)
        tree = parser.parse()

        if not tree:
            print("No exit statement found")
            return EXIT_FAILURE

        generator = Generator(tree)

        output = generator.generate()

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
