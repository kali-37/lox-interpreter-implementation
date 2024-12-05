from typing import Dict
from typing import List
from typing import Optional

EOF_INDICATOR = "EOF  null"

character_tokens: Dict[str, str] = {
    "(": "LEFT_PAREN",
    ")": "RIGHT_PAREN",
}


def scan_token(content: str) -> List[str]:
    result: List[str] = []
    for char in content:
        current_token:Optional[str]= character_tokens.get(char, None)
        if current_token:
            result.append(f"{current_token} {char} null")
    result.append(EOF_INDICATOR)
    return result