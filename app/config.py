from enum import IntEnum


class ExitCode(IntEnum):
    SUCCESS = 0
    FAILURE = 1
    EX_DATAERR = 65
    EX_SOFTWARE = 70
