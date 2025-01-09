import logging
import threading
import time


def thread_function(name):
    logging.info("Thread [1]: starting, INDENT : %s", threading.get_ident())
    for i in range(4):
        logging.info(f"THread 1 {i}")
        time.sleep(0.6)
    logging.info("Thread [1]: finishing ,  %s", threading.get_ident())


def thread_function_2(name):
    logging.info("Thread[2] :%s starting ", threading.get_ident())
    for i in range(4):
        logging.info(f"THread 2 {i}")
        time.sleep(0.2)
    logging.info("Thread[2] : %s finishing", threading.get_ident())


import concurrent.futures
from typing import Callable, Generator, TypeVar

_T = TypeVar("_T")
print("NAME ", __name__)

if __name__ == "__main__":
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")

    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        executor.map(
            lambda x: x[1](x[0]),
            enumerate(
                [thread_function, thread_function_2, thread_function, thread_function_2]
            ),
        )
