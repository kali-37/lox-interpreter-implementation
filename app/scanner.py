from typing import List, Optional, Tuple

from app.config import ExitCode, character_tokens, equal_sign_preceeder
from app.error import LogError
from app.tokens import Token, TokenType, ignore_tokens


class Scanner:
    def __init__(self, source: List[str], column: int = 0, row: int = 0):
        self.source = source
        self.current_line: str = ""
        self.column: int = column
        self.row: int = row
        self.tokens: list[Token] = []
        self.exit_status = ExitCode.SUCCESS

    def is_not_end_column(self, column: Optional[int] = None) -> bool:
        if column:
            return column < len(self.source)
        return self.column < len(self.source)

    def is_not_end_row(self, row: Optional[int] = None) -> bool:
        if row:
            return row < len(self.current_line)
        return self.row < len(self.current_line)

    def is_ignore_character(self) -> bool:
        return self.current_line[self.row] in ignore_tokens

    def get_token_name(self, token_symbol: str) -> Optional[str]:
        return (
            TokenType(token_symbol).name
            if TokenType.has_token_symbol(token_symbol)
            else None
        )

    def validate_ignoreable_token(self, token_symbol: str) -> None:
        if not self.is_ignore_character():
            LogError(self.column, token_symbol).display_error()
            self.exit_status = ExitCode.EX_DATAERR

    def is_comment_signature(self, token_symbol: str):
        return (
            token_symbol == "/"
            and self.is_not_end_row(self.row + 1)
            and self.current_line[self.row + 1] == "/"
        )

    def is_equal_sign_preceeder(self, token_symbol: str) -> bool:
        return (
            (token_symbol in equal_sign_preceeder)
            and self.is_not_end_row(self.row + 1)
            and self.current_line[self.row + 1] == "="
        )

    def scan_tokens(self) -> Tuple[List[Token], ExitCode]:
        while self.is_not_end_column():
            self.current_line = self.source[self.column]
            while self.is_not_end_row():
                token_symbol = self.current_line[self.row]
                token_name: Optional[str] = self.get_token_name(token_symbol)
                if not token_name:
                    self.validate_ignoreable_token(token_symbol)
                else:
                    if self.is_equal_sign_preceeder(token_symbol):
                        token_symbol += "="
                        token_name = character_tokens.get(token_symbol)
                        self.row += 1

                    # Break the current line on encountering a comment flow
                    if self.is_comment_signature(token_symbol):
                        break
                    self.tokens.append(
                        Token(TokenType(token_symbol).name, token_symbol, None)
                    )
                self.row += 1
            self.column += 1
            self.row = 0
        self.tokens.append(Token(TokenType("").name, "", None))
        return self.tokens, self.exit_status


# EOF  null
# EOF  null
# EOF  null

# "EOF  null"
# "EOF   null"
# "EOF  null"
