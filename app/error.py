import sys

# from app.logger import logging


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
