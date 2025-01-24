from app.tokens import TokenType
from app.expression import Expr
from app.expression import Expression
from app.statments import Stmt
from typing import Any
from typing import Optional, Union


class Interpreter(Expr):
    def visitBinaryExpr(self, expr: Expression.Binary):
        left = self.evaluate(expr.left)
        right = self.evaluate(expr.right)
        if expr.operator.token_type_ == TokenType.MINUS.name:
            return left - right
        elif expr.operator.token_type_ == TokenType.PLUS.name:
            return left + right
        elif expr.operator.token_type_ == TokenType.SLASH.name:
            return left / right
        elif expr.operator.token_type_ == TokenType.STAR.name:
            return left * right
        elif expr.operator.token_type_ == TokenType.GREATER.name:
            return left > right
        elif expr.operator.token_type_ == TokenType.GREATER_EQUAL.name:
            return left >= right
        elif expr.operator.token_type_ == TokenType.LESS.name:
            return left < right
        elif expr.operator.token_type_ == TokenType.LESS_EQUAL.name:
            return left <= right
        elif expr.operator.token_type_ == TokenType.BANG_EQUAL.name:
            return left != right
        elif expr.operator.token_type_ == TokenType.EQUAL_EQUAL.name:
            return left == right
        else:
            return None

    def visitGroupingExpr(self, expr: Expression.Group):
        return self.evaluate(expr.expression)

    def visitLiteralExpr(self, expr: Expression.Literal):
        return expr.value

    def visitUnaryExpr(self, expr: Expression.Unary):
        right = self.evaluate(expr.right)
        if self.is_digit(right):
            right = self.is_digit(right, realType=True)
        if expr.operator.token_type_ == TokenType.MINUS.name:
            return -right
        elif expr.operator.token_type_ == TokenType.BANG.name:
            return not self.is_truthy(right)
        else:
            return None

    def is_truthy(self, obj: object):
        if obj is None:
            return False
        if isinstance(obj, bool):
            return obj
        return True

    def evaluate(self, expr: Optional[Expr]) -> Any:
        if expr == None:
            return None
        if isinstance(expr, Expression.Literal):
            return self.visitLiteralExpr(expr)
        if isinstance(expr, Expression.Group):
            return self.visitGroupingExpr(expr)
        if isinstance(expr, Expression.Binary):
            return self.visitBinaryExpr(expr)
        # if type(expr) == Expr.Call:
        # return self.evalCall(expr, printAllExpressions)
        if isinstance(expr, Expression.Unary):
            return self.visitUnaryExpr(expr)
        # if type(expr) == Expr.Logical:
        # return self.evalLogical(expr)
        # if type(expr) == Expr.Variable:
        # return self.evalVariable(expr)
        # if type(expr) == Expr.Assign:
        # return self.evalAssignment(expr)

    #

    def stringify(self, obj: Any) -> str:
        if obj == None:
            return "nil"
        if type(obj) == float:
            if str(obj).endswith(".0"):
                return str(int(obj))
        if type(obj) == bool:
            return str(obj).lower()

        return str(obj)

    def execute(self, statment: Stmt):
        print(self.stringify(self.evaluate(statment.expression)))

    def interpret(self, statment: Stmt):
        self.execute(statment)
