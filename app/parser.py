"""
expression     → literal
               | unary
               | binary
               | grouping ;

literal        → NUMBER | STRING | "true" | "false" | "nil" ;
grouping       → "(" expression ")" ;
unary          → ( "-" | "!" ) expression ;
binary         → expression operator expression ;
operator       → "==" | "!=" | "<" | "<=" | ">" | ">="
               | "+"  | "-"  | "*" | "/" ;

expression     → equality ;
equality       → comparison ( ( "!=" | "==" ) comparison )* ;
comparison     → term ( ( ">" | ">=" | "<" | "<=" ) term )* ;
term           → factor ( ( "-" | "+" ) factor )* ;
factor         → unary ( ( "/" | "*" ) unary )* ;
unary          → ( "!" | "-" ) unary
               | primary ;
primary        → NUMBER | STRING | "true" | "false" | "nil"
               | "(" expression ")" ;

"""

from app.tokens import Token
from app.tokens import TokenType
from app.expression import Expr
from typing import List
from app.error import LoxError
from app.scanner import Scanner
from app.expression import Expression
from app.statments import Stmt


class Parser:
    _current: int = 0
    parsed_list: List[Expr] = []

    def parse(self):
        try:
            return Stmt(self.expression())
        except RuntimeError as e:
            print(e)
            return

    def __init__(self, final: List[str]):
        self._final = Scanner(final).scan_tokens()

    def expression(self):
        return self.equality()

    def is_at_end(self) -> bool:
        return self.peek().token_type_ == TokenType.EOF

    def peek(self) -> Token:
        return self._final[self._current]

    def previous(self) -> Token:
        return self._final[self._current - 1]

    def check(self, type: TokenType) -> bool:
        if self.is_at_end():
            return False
        return str(self.peek().token_type_) == type.name

    def consume(self, type: TokenType, message: str):
        if self.check(type):
            return self.advance()
        LoxError.error(self.peek(), message)

    def advance(self) -> Token:
        if not self.is_at_end():
            self._current += 1
        return self.previous()

    def match(self, *types: TokenType) -> bool:
        for type in types:
            if self.check(type):
                self.advance()
                return True
        return False

    def primary(self) -> Expr:
        if self.match(TokenType.FALSE):
            return Expression.Literal(False)

        if self.match(TokenType.TRUE):
            return Expression.Literal(True)

        if self.match(TokenType.NIL):
            return Expression.Literal(None)

        if self.match(TokenType.NUMBER, TokenType.STRING):
            return Expression.Literal(self.previous().literal_)

        if self.match(TokenType.LEFT_PAREN):
            expr = self.expression()
            self.consume(TokenType.RIGHT_PAREN, "Expect ')' after expression.")
            return Expression.Group(expr)
        raise LoxError.error(self.peek(), "Expect expression.")

    def unary(self) -> Expr:
        while self.match(TokenType.BANG, TokenType.MINUS):
            operator = self.previous()
            right = self.unary()
            return Expression.Unary(operator, right)
        return self.primary()

    def factor(self) -> Expr:
        expr = self.unary()
        while self.match(TokenType.SLASH, TokenType.STAR):
            operator = self.previous()
            right = self.unary()
            expr = Expression.Binary(expr, operator, right)
        return expr

    def term(self) -> Expr:
        expr: Expr = self.factor()
        while self.match(TokenType.MINUS, TokenType.PLUS):
            operator = self.previous()
            right = self.factor()
            expr = Expression.Binary(expr, operator, right)
        return expr

    def comparison(self):
        expr: Expr = self.term()
        while self.match(
            TokenType.GREATER,
            TokenType.GREATER_EQUAL,
            TokenType.LESS,
            TokenType.LESS_EQUAL,
        ):
            operator = self.previous()
            right = self.term()
            expr = Expression.Binary(expr, operator, right)
        return expr

    def equality(self):
        expr = self.comparison()

        while self.match(TokenType.BANG_EQUAL, TokenType.EQUAL_EQUAL):
            operator = self.previous()
            right = self.comparison()
            expr = Expression.Binary(expr, operator, right)
        return expr
