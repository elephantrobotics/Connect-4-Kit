# @author  : Zhu ZhenDong
# @time    : 2023-06-15 05-53-03
# @function:
# @version :

import logging
import sys
from pathlib import Path

log_path = Path("./logs/app.log")
formatter = logging.Formatter("%(levelname)s - %(asctime)s - %(name)s - %(message)s")


def get_logger(name, level=logging.DEBUG, filepath=log_path):
    """This function is used to get a logger with a specific name and level
    The logger will output to the standard output (console)
    The output format of the logger is: level - time - name - message
    name: the name of the logger
    level: the level of the logger
    return: a logger with the specified name and level"""

    logger: logging.Logger = logging.getLogger(name)
    logger.propagate = False
    logger.level = level

    # add std handler
    std_hdlr = logging.StreamHandler(sys.stdout)
    std_hdlr.setLevel(level)
    std_hdlr.setFormatter(formatter)
    logger.addHandler(std_hdlr)

    # add file handler
    file_hdlr = logging.FileHandler(filepath)
    file_hdlr.setFormatter(formatter)
    logger.addHandler(file_hdlr)
    return logger
