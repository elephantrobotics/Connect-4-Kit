# @author  : Zhu ZhenDong
# @time    : 2023-06-15 05-53-03
# @function:
# @version :

import logging
import sys


def get_logger(name, level):
"""     This function is used to get a logger with a specific name and level
    The logger will output to the standard output (console)
    The output format of the logger is: level - time - name - message
    name: the name of the logger
    level: the level of the logger
    return: a logger with the specified name and level"""
    logger = logging.getLogger(name)
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(level)
    formatter = logging.Formatter(
        "%(levelname)s - %(asctime)s - %(name)s - %(message)s"
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger
