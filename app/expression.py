# from typing import List
from app.tokens import Token


class Expr:
    def __repr__(self) -> str:
        return self.__str__()


class Group(Expr):
    def __init__(self, expression: str):
        self.expression = expression

    def __str__(self) -> str:
        return f"(group {str(self.expression)})"


class Unary(Expr):
    def __init__(self, operator: Token, right: Expr):
        self.operator = operator
        self.right = right

    def __str__(self) -> str:
        return f"({self.operator.lexeme_} {self.right})"
