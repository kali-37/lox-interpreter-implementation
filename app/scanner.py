import sys
from typing import Dict
from typing import List
from typing import Optional
from typing import Set
from typing import Tuple

from app.config import ExitCode

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


def scan_token(content: List[str]) -> Tuple[List[str], Optional[int]]:
    result: List[str] = []
    exit_status: Optional[ExitCode] = None
    line_no: int = 0
    while line_no < len(content):
        line = content[line_no]
        column_no: int = 0
        while column_no < len(line):
            token_symbol = line[column_no]
            token_name: Optional[str] = character_tokens.get(
                token_symbol, None
            )

            if not token_name:
                # logging.error(f"[line {line_no+1}] Error: Unexpected character: {token_symbol}")
                if token_symbol not in ignore_characters:
                    print(
                        f"[line {line_no+1}] Error: Unexpected character: {token_symbol}",
                        file=sys.stderr,
                    )
                    exit_status = ExitCode.EX_DATAERR

            else:
                # Case : comparison operation preceding (=) sign
                if (
                    (token_symbol in equal_sign_preceeder)
                    and column_no + 1 < len(line)
                    and line[column_no + 1] == "="
                ):
                    token_symbol += "="
                    token_name = character_tokens.get(token_symbol)
                    column_no += 1

                # Break the current line on encountering a comment flow
                if (
                    token_symbol == "/"
                    and column_no + 1 < len(line)
                    and line[column_no + 1] == "/"
                ):
                    break

                result.append(f"{token_name} {token_symbol} null")
            column_no += 1
        line_no += 1
    result.append(EOF_INDICATOR)
    return result, exit_status
