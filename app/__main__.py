import argparse
import os
from argparse import Namespace
from typing import List
from typing import Iterable

from app.config import ExitCode
from app.logger import logger
from app.scanner import Scanner
from app.tokens import Token
from app.tokens import TokenType
from app.parser import Parser
from app.error import LoxError
from app.interpreter import Interpreter


def parse_argument():
    parser = argparse.ArgumentParser(
        usage="Usage: ./your_program.sh tokenize <filename>",
        description="Provide a filename to tokenize it.",
    )
    parser.add_argument("action", type=str, help="tokenize|parse arg required")
    parser.add_argument("filename", type=str, help="filename required")
    args = parser.parse_args()
    return args


def parse_file_content(file_contents: List[str], evaluate: bool = False):
    LoxError.hadError = False
    LoxError.hadRuntimeError = False
    parsed_tokens = Parser(file_contents).parse()
    if evaluate:
        return parsed_tokens
    if parsed_tokens:
        print(parsed_tokens)
    if LoxError.hadError:
        exit(ExitCode.EX_DATAERR)
    if LoxError.hadRuntimeError:
        exit(ExitCode.EX_SOFTWARE)


def scan_file_contents(file_contents: List[str]):
    obj = Scanner(file_contents)
    iterable_lexeme: Iterable[Token] = obj.scan_tokens()
    for lexeme in iterable_lexeme:
        print(lexeme)
    if obj.exit_status:
        exit(obj.exit_status.value)


def evaluate(file_contents: List[str]):
    LoxError.hadRuntimeError=False
    parsed_content = parse_file_content(file_contents, evaluate=True)
    if parsed_content:
        Interpreter().interpret(parsed_content)
    if LoxError.hadRuntimeError:
        exit(ExitCode.EX_SOFTWARE)


def main(args: Namespace):
    logger.debug("Logs from your program will appear here!")

    if args.action not in ["tokenize", "parse", "evaluate"]:
        logger.warning(f"Unknown command: {args.action}")
        exit(ExitCode.FAILURE)

    if not os.path.exists(args.filename):
        logger.error("File Dosen't exists")
        exit(ExitCode.FAILURE)

    with open(args.filename) as file:
        file_contents = file.readlines()
    if file_contents:
        if args.action == "parse":
            parse_file_content(file_contents)
        elif args.action == "evaluate":
            evaluate(file_contents)
        else:
            scan_file_contents(file_contents)

    else:
        # logger.info(EOF_INDICATOR)
        print(Token(TokenType("").name, "", None))


if __name__ == "__main__":
    main(parse_argument())
