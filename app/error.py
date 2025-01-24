import sys
from app.tokens import Token
from app.tokens import TokenType
from typing import Any

# from app.logger import logging


class ParseErro(RuntimeError):
    pass


class LuxRunTimeError(RuntimeError):
    def __init__(self, token: Any, errno: str):
        super().__init__(errno)
        self.token = token


class ParseError:
    hadError = False
    hadRuntimeError = False

    @staticmethod
    def error(tokenType: Token, message: str):
        tokenType = tokenType
        message = message
        ParseError.hadError = True
        if tokenType.token_type_ == TokenType.EOF:
            print(
                f"[line {tokenType.line}] Error at end: {message}",
                file=sys.stderr,
            )
        else:
            print(
                f"[line {tokenType.line}] Error at '{tokenType.lexeme_}': {message}",
                file=sys.stderr,
            )
        raise ParseErro()


class LogError:
    def __init__(self, error_column: int, token_symbol: str):
        self.error_column = error_column
        self.token_symbol = token_symbol

    def display_token_error(self):
        print(
            f"[line {self.error_column+1}] Error: Unexpected character: {self.token_symbol}",
            file=sys.stderr,
        )
        # logging.error(
        # f"[line {self.error_column+1}] Error: Unexpected character: {self.token_symbol}",
        # )

    def display_literal_error(self):
        print(
            f"[line {self.error_column+1}] Error: Unterminated string.",
            file=sys.stderr,
        )
        # logging.error(
        # f"[line {self.error_column+1}] Error: Unterminated string.",
        # )
