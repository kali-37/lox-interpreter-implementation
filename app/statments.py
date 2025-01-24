from app.expression import Expr


class Stmts:
    def __repr__(self) -> str:
        return self.__str__()


class Stmt(Stmts):
    def __init__(self, expression: Expr):
        self.expression = expression

    def __str__(self) -> str:
        return str(self.expression)
