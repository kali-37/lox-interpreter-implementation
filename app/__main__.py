import argparse
import os
from argparse import Namespace
from enum import IntEnum

from app.logger import logger
from app.scanner import EOF_INDICATOR
from app.scanner import scan_token


class ExitStatus(IntEnum):
    SUCESS = 0
    FAILURE = 1


def parse_argument():
    parser = argparse.ArgumentParser(
        usage="Usage: ./your_program.sh tokenize <filename>",
        description="Provide a filename to tokenize it.",
    )
    parser.add_argument("tokenize", type=str, help="tokenize arg required")
    parser.add_argument("filename", type=str, help="filename required")
    args = parser.parse_args()
    return args


def main(args: Namespace):
    logger.debug("Logs from your program will appear here!")

    if args.tokenize != "tokenize":
        logger.warning(f"Unknown command: {args.tokenize}")
        exit(ExitStatus.FAILURE)

    if not os.path.exists(args.filename):
        logger.error("File Dosen't exists")
        exit(ExitStatus.FAILURE)

    with open(args.filename) as file:
        file_contents = file.read()
    if file_contents:
        for lexeme in scan_token(file_contents):
            print(lexeme)

    else:
        # logger.info(EOF_INDICATOR)
        print(EOF_INDICATOR)


if __name__ == "__main__":
    main(parse_argument())
