# from typing import List
from app.tokens import Token


class Expr:
    def __repr__(self) -> str:
        return self.__str__()


class Group(Expr):
    def __init__(self, expression:Expr):
        self.expression = expression

    def __str__(self) -> str:
        return f"(group {str(self.expression)})"


class Unary(Expr):
    def __init__(self, operator: Token, right:Expr):
        self.operator = operator
        self.right = right

    def __str__(self) -> str:
        return f"({self.operator.lexeme_} {self.right})"


class Binary(Expr):
    def __init__(self, left:Expr , operator: Token, right:Expr):
        self.left = left
        self.operator = operator
        self.right = right

    def __str__(self):
        return f"({self.operator.lexeme_} {self.left} {self.right})"
 
class Literal(Expr):
    def __init__(self, value: object):
        self.value = value
    
    def __str__(self) -> str:
        if (self.value == None):
            return "nil"
        if (type(self.value) == bool):
            return str(self.value).lower()
            
        return str(self.value) 