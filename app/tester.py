from typing import Optional


class Stackchecker:
    def __init__(self):
        self.stack_elems: str = ""

    def add_elements(self, number: str):
        self.stack_elems += number


def stacker(i: str, stack: Optional[Stackchecker] = None):
    if stack is None:
        stack = Stackchecker()
    stack.add_elements(i)
    print(stack.stack_elems)


for i in range(5):
    stacker(f"{i}")
