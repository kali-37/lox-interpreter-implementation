from enum import Enum
from typing import Optional
from typing import Set

equal_sign_preceeder: Set[str] = {"=", "!", ">", "<"}
ignore_tokens: Set[str] = {" ", "\t", "\n"}
string_literals: Set[str] = {'"'}


class TokenType(Enum):
    LEFT_PAREN = "("
    RIGHT_PAREN = ")"
    LEFT_BRACE = "{"
    RIGHT_BRACE = "}"
    COMMA = ","
    DOT = "."
    MINUS = "-"
    PLUS = "+"
    SEMICOLON = ";"
    SLASH = "/"
    STAR = "*"
    BANG = "!"
    EQUAL = "="
    GREATER = ">"
    LESS = "<"

    # multi character tokens
    BANG_EQUAL = "!="
    EQUAL_EQUAL = "=="
    GREATER_EQUAL = ">="
    LESS_EQUAL = "<="

    # String literals
    STRING =  "nan" # STRING starts with <"> character so,
    NUMBER = (0, 1, 2, 4, 5, 6, 7, 8, 9)

    # Identifiers
    IDENTIFIER = "null"

    EOF = ""

    @classmethod
    def has_token_symbol(cls, token_symbol: str) -> bool:
        return token_symbol in cls._value2member_map_

    @classmethod
    def get_token_name(cls, token_symbol: str) -> Optional[str]:
        if cls.has_token_symbol(token_symbol):
            return cls(token_symbol).name
        return None

    def __repr__(self) -> str:
        return f"{self.name}"


class Token:
    def __init__(
        self, token_type: str, lexeme: str, literal: Optional[str] = None
    ) -> None:
        self.token_type: str = token_type
        self.lexeme: str = lexeme
        self.literal: Optional[str] = literal if literal else "null"

    def __str__(self) -> str:
        return f"{self.token_type} {self.lexeme} {self.literal}"

    def __repr__(self) -> str:
        return self.__str__()
