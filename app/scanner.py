from app.config import ExitCode
from app.error import LogError
from app.tokens import KEYWORDS, Token
from app.tokens import TokenType
from app.tokens import equal_sign_preceeder
from app.tokens import ignore_tokens
from app.tokens import string_literals
from typing import List, Optional


ESCAPE_SEQUENCE = [r"\s", "\t", "\n"]


class Stack:
    def __init__(
        self, boundary_capturer: List[str] = [], buffer: str = ""
    ) -> None:
        """
        Example  for string : "hello" ,the boundary capturer will be ['"'] and buffer will be hello
        """
        self.boundary_capturer: List[str] = boundary_capturer
        self.inner_elements: str = buffer
        self.is_active = False

    def is_empty(self):
        return not self.boundary_capturer

    def push_capturer(self, element: str) -> None:
        self.is_active = True
        self.boundary_capturer.append(element)

    def push_element(self, element: str) -> None:
        self.inner_elements += element

    def pop_capturer(self) -> str:
        if self.boundary_capturer:
            return self.boundary_capturer.pop()
        else:
            self.is_active = False
            return ""

    def reset_stack(self):
        self.boundary_capturer = []
        self.inner_elements = ""
        self.is_active = False


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

    def validate_ignoreable_token(self, token_symbol: str) -> bool:
        if not self.is_ignore_character():
            LogError(self.column, token_symbol).display_token_error()
            self.exit_status = ExitCode.EX_DATAERR
            return True
        return False

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

    def include_scanned_tokens(
        self,
        token_symbol: str,
        token_name: str = "",
        literal: Optional[str] = None,
    ):
        self.tokens.append(
            Token(
                token_name if token_name else TokenType(token_symbol).name,
                token_symbol,
                literal if literal else None,
            )
        )

    def handel_string_literals(
        self, token_symbol: str, stack: Optional[Stack] = None
    ):
        if stack is None:
            stack = Stack()
        upcomming_symbol = ""
        stack.boundary_capturer.append(token_symbol)
        self.row += 1
        while self.is_not_end_row() and upcomming_symbol != token_symbol:
            stack.inner_elements += upcomming_symbol
            upcomming_symbol = self.current_line[self.row]
            self.row += 1
        self.row -= 1
        if upcomming_symbol == token_symbol:
            token_symbol = (
                token_symbol + stack.inner_elements + stack.pop_capturer()
            )
            token_name = TokenType.STRING.name
            literal = stack.inner_elements
            self.include_scanned_tokens(token_symbol, token_name, literal)

        else:
            LogError(self.column, token_symbol).display_literal_error()
            self.exit_status = ExitCode.EX_DATAERR
            return

    def handel_numeric_literals(
        self, token_symbol: str, stack: Optional[Stack] = None
    ):
        if stack is None:
            stack = Stack()

        def recognize_numerics(token_symbol: str, stack: Stack):
            while self.is_not_end_row(self.row) and token_symbol.isdigit():
                stack.inner_elements += self.current_line[self.row]
                self.row += 1
                if not self.is_not_end_row(self.row):
                    break
                token_symbol = self.current_line[self.row]

        recognize_numerics(token_symbol, stack)

        if (
            self.is_not_end_row(self.row)
            and self.is_not_end_row(self.row + 1)
            and self.current_line[self.row] == "."
            and self.current_line[self.row + 1].isdigit()
        ):
            stack.inner_elements += "."
            self.row += 1
            recognize_numerics(token_symbol, stack)
        self.row -= 1
        stack_elem = stack.inner_elements
        return self.include_scanned_tokens(
            stack_elem, TokenType.NUMBER.name, str(float(stack.inner_elements))
        )

    def handel_identifiers(self, token_symbol: str) -> None:
        """IT handels identifiers and also the keywords  as they are related"""
        identifier = ""
        while True:
            if (
                self.is_not_end_row(self.row + 1)
                and (token_symbol.isalnum() or token_symbol == "_")
                and token_symbol not in ignore_tokens
            ):
                identifier += token_symbol
                self.row += 1
                token_symbol = self.current_line[self.row]
            else:
                break

        if not self.is_not_end_row(self.row + 1) and (
            token_symbol.isalnum() or token_symbol == "_"
        ):
            identifier += token_symbol
        else:
            self.row -= 1
        token_name = TokenType.IDENTIFIER.name
        if identifier in KEYWORDS.keys():
            token_name = KEYWORDS[identifier].name
        return self.include_scanned_tokens(
            identifier,
            token_name,
            "null",
        )

    def enquire_token_type(self, token_symbol: str) -> None:
        token_name = ""
        if token_symbol in string_literals:
            return self.handel_string_literals(token_symbol)

        elif self.is_equal_sign_preceeder(token_symbol):
            token_symbol += "="
            token_name = TokenType(token_symbol).name
            self.row += 1

        elif token_symbol.isdigit():
            return self.handel_numeric_literals(token_symbol)

        elif token_symbol.isalpha() or token_symbol == "_":
            return self.handel_identifiers(token_symbol)

        elif not TokenType.has_token_symbol(token_symbol):
            self.validate_ignoreable_token(token_symbol)
            return

        self.include_scanned_tokens(token_symbol, token_name, None)

    def scan_individual_line(self) -> None:
        while self.is_not_end_row():
            token_symbol = self.current_line[self.row]
            # Check if the token is an ignoreable character
            if token_symbol in ignore_tokens:
                pass
            # if not token_name and not token_symbol.isdigit():
            # self.validate_ignoreable_token(token_symbol)
            # Break the current line on encountering a comment signature
            elif self.is_comment_signature(token_symbol):
                break
            # Enquire the token type and add accordingly
            else:
                self.enquire_token_type(token_symbol)
            self.row += 1

    def scan_tokens(self) -> List[Token]:
        while self.is_not_end_column():
            self.current_line = self.source[self.column]
            self.scan_individual_line()  # Second while loop
            self.column += 1
            # Reset the row counter for the next line
            self.row = 0
        self.tokens.append(Token(TokenType("").name, "", None))
        return self.tokens
