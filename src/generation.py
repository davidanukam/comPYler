from macros import *

from nodes import NodeExit


class Generator:
    def __init__(self, root: NodeExit):
        self.root = root

    def generate(self) -> str:
        output = (
            f"bits 64\n\ndefault rel\nextern ExitProcess\n\nglobal _start:\n\n_start:\n"
        )

        # output += f"    mov rax, 60\n"
        # output += f"    mov rdi, {self.root.expr.int_lit.value}\n"
        # output += f"    syscall"
        output += f"    sub rsp, 40\n"
        output += f"    xor rcx, rcx\n"
        output += f"    call ExitProcess"

        return output
