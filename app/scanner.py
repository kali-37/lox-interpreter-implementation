import sys
from typing import Dict
from typing import List
from typing import Optional
from typing import Tuple

from app.config import ExitCode

EOF_INDICATOR = "EOF  null"

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
    ";": "SEMICOLON",
}


def scan_token(content: List[str]) -> Tuple[List[str],Optional[int]]:
    result: List[str] = []
    exit_status = None 
    for line_no, line in enumerate(content):
        for char in line:
            current_token: Optional[str] = character_tokens.get(char, None)
            if not current_token:
                # logging.error(f"[line {line_no+1}] Error: Unexpected character: {char}")
                print(f"[line {line_no+1}] Error: Unexpected character: {char}",file=sys.stderr)
                exit_status = ExitCode.EX_DATAERR
            else:
                result.append(f"{current_token} {char} null")
    result.append(EOF_INDICATOR)
    return result,exit_status
