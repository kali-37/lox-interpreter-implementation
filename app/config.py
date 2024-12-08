from enum import IntEnum
from typing import Dict, Set


class ExitCode(IntEnum):
    SUCCESS = 0
    FAILURE = 1
    EX_DATAERR = 65


EOF_INDICATOR = "EOF  null"
equal_sign_preceeder: Set[str] = {"=", "!", ">", "<"}
ignore_characters: Set[str] = {" ", "\t", "\n"}


character_tokens: Dict[str, str] = {
    "(": "LEFT_PAREN",
    ")": "RIGHT_PAREN",
    "{": "LEFT_BRACE",
    "}": "RIGHT_BRACE",
    "*": "STAR",
    ".": "DOT",
    ",": "COMMA",
    "+": "PLUS",
    "-": "MINUS",
    "*": "STAR",
    "==": "EQUAL_EQUAL",
    "=": "EQUAL",
    ";": "SEMICOLON",
    "!": "BANG",
    "!=": "BANG_EQUAL",
    "<": "LESS",
    ">": "GREATER",
    "<=": "LESS_EQUAL",
    ">=": "GREATER_EQUAL",
    "/": "SLASH",
    "*": "STAR",
}
