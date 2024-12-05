import argparse
import os
from argparse import Namespace

from app.config import ExitCode
from app.logger import logger
from app.scanner import EOF_INDICATOR
from app.scanner import scan_token


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
        exit(ExitCode.FAILURE)

    if not os.path.exists(args.filename):
        logger.error("File Dosen't exists")
        exit(ExitCode.FAILURE)

    with open(args.filename) as file:
        file_contents = file.readlines()
    if file_contents:
        scan_status = scan_token(file_contents)
        for lexeme in scan_status[0]:
            print(lexeme)
        if scan_status[1]: 
            exit(scan_status[1])

    else:
        # logger.info(EOF_INDICATOR)
        print(EOF_INDICATOR)


if __name__ == "__main__":
    main(parse_argument())
