# @author  : Zhu ZhenDong
# @time    : 2023-06-15 05-53-03
# @function:
# @version :

import logging
import sys


def get_logger(name, level):
    logger = logging.getLogger(name)
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(level)
    formatter = logging.Formatter(
        "%(levelname)s - %(asctime)s - %(name)s - %(message)s"
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger
