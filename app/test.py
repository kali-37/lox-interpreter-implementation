from typing import Callable
from typing import Dict
from typing import List
from typing import Optional

from app.lox import Lox
from app.token import Token

# type: ignore all
from app.token_type import TokenType


class Scanner:
    def __init__(self, source: str):
        self.source: str = source
        self.tokens: List[Token] = []
        self.start: int = 0
        self.current: int = 0
        self.line: int = 1
        self.token_actions: Dict[str, Callable[[], None]] = {
            "(": lambda: self.add_token(TokenType.LEFT_PAREN),
            ")": lambda: self.add_token(TokenType.RIGHT_PAREN),
            "{": lambda: self.add_token(TokenType.LEFT_BRACE),
            "}": lambda: self.add_token(TokenType.RIGHT_BRACE),
            ",": lambda: self.add_token(TokenType.COMMA),
            ".": lambda: self.add_token(TokenType.DOT),
            "-": lambda: self.add_token(TokenType.MINUS),
            "+": lambda: self.add_token(TokenType.PLUS),
            ";": lambda: self.add_token(TokenType.SEMICOLON),
            "*": lambda: self.add_token(TokenType.STAR),
            "!": lambda: self.add_token(
                TokenType.BANG_EQUAL if self.match("=") else TokenType.BANG
            ),
            "=": lambda: self.add_token(
                TokenType.EQUAL_EQUAL if self.match("=") else TokenType.EQUAL
            ),
            "<": lambda: self.add_token(
                TokenType.LESS_EQUAL if self.match("=") else TokenType.LESS
            ),
            ">": lambda: self.add_token(
                TokenType.GREATER_EQUAL
                if self.match("=")
                else TokenType.GREATER
            ),
            "/": self.handle_slash,
            '"': self.handle_string,
        }

    def scan_tokens(self) -> List[Token]:
        while not self.is_at_end():
            self.start = self.current
            self.scan_token()
        self.tokens.append(Token(TokenType.EOF, "", None, self.line))
        return self.tokens

    def is_at_end(self) -> bool:
        return self.current >= len(self.source)

    def scan_token(self) -> None:
        c: str = self.advance()
        if action := self.token_actions.get(c):
            action()
        elif c.isspace():
            if c == "\n":
                self.line += 1
        else:
            Lox.error(self.line, f"Unexpected character: {c}")

    def handle_slash(self) -> None:
        if self.match("/"):
            # A comment goes until the end of the line.
            while self.peek() != "\n" and not self.is_at_end():
                self.advance()
        else:
            self.add_token(TokenType.SLASH)

    def handle_string(self) -> None:
        while self.peek() != '"' and not self.is_at_end():
            if self.peek() == "\n":
                self.line += 1
            self.advance()
        if self.is_at_end():
            Lox.error(self.line, "Unterminated string.")
            return
        # The closing ".
        self.advance()
        # Trim the surrounding quotes.
        value = self.source[self.start + 1 : self.current - 1]
        self.add_token(TokenType.STRING, value)

    def advance(self) -> str:
        self.current += 1
        return self.source[self.current - 1]

    def match(self, expected: str) -> bool:
        if self.is_at_end() or self.source[self.current] != expected:
            return False
        self.current += 1
        return True

    def add_token(
        self, type: TokenType, literal: Optional[object] = None
    ) -> None:
        text: str = self.source[self.start : self.current]
        self.tokens.append(Token(type, text, literal, self.line))

    def peek(self) -> str:
        return "\0" if self.is_at_end() else self.source[self.current]

    def peek_next(self) -> str:
        if self.current + 1 >= len(self.source):
            return "\0"
        return self.source[self.current + 1]
