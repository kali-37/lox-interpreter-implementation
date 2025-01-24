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
    STRING = "nan"  # STRING starts with <"> character so,
    NUMBER = (0, 1, 2, 4, 5, 6, 7, 8, 9)

    # Identifiers
    IDENTIFIER = "null"

    EOF = ""

    AND = "and"
    CLASS = "class"
    ELSE = "else"
    FALSE = "false"
    FUN = "fun"
    FOR = "for"
    IF = "if"
    NIL = "nil"
    OR = "or"
    PRINT = "print"
    RETURN = "return"
    SUPER = "super"
    THIS = "this"
    TRUE = "true"
    VAR = "var"
    WHILE = "while"

    def __str__(self) -> str:
        return self.name

    @classmethod
    def has_token_symbol(cls, token_symbol: str) -> bool:
        return token_symbol in cls._value2member_map_

    @classmethod
    def get_token_name(cls, token_symbol: str) -> Optional[str]:
        if cls.has_token_symbol(token_symbol):
            return cls(token_symbol).name
        return None

    def __repr__(self):
        return f"{self.name}"


class Token:
    def __init__(
        self,
        token_type: TokenType,
        lexeme: str,
        literal: Optional[str] = None,
        line: int = 0,
    ) -> None:
        self.token_type_: TokenType = token_type
        self.lexeme_: str = lexeme
        self.literal_: Optional[str] = (
            literal if isinstance(literal, (float, str)) else "null"
        )
        self.line: int = line

    def __str__(self) -> str:
        return f"{self.token_type_} {self.lexeme_} {self.literal_}"

    def __repr__(self) -> str:
        return self.__str__()


KEYWORDS = {
    "and": TokenType.AND,
    "class": TokenType.CLASS,
    "else": TokenType.ELSE,
    "false": TokenType.FALSE,
    "fun": TokenType.FUN,
    "for": TokenType.FOR,
    "if": TokenType.IF,
    "nil": TokenType.NIL,
    "or": TokenType.OR,
    "print": TokenType.PRINT,
    "return": TokenType.RETURN,
    "super": TokenType.SUPER,
    "this": TokenType.THIS,
    "true": TokenType.TRUE,
    "var": TokenType.VAR,
    "while": TokenType.WHILE,
}
