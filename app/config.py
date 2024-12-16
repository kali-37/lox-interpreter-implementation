from enum import IntEnum
from typing import Dict
from typing import Set


class ExitCode(IntEnum):
    SUCCESS = 0
    FAILURE = 1
    EX_DATAERR = 65
