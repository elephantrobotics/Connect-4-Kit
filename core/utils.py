import platform
import os
from enum import Enum, auto
import subprocess
from typing import List

def exec_shell(cmd : List[str]) -> str:
    result = subprocess.run(cmd, stdout=subprocess.PIPE)
    return result.stdout.decode("utf-8")

class Platform(Enum):
    WINDOWS = auto()
    JETSON_NANO = auto()
    RASPBERRY_PI = auto()

class SystemIdentity:
    @staticmethod
    def is_jetson_nano():
        if SystemIdentity.is_linux():
            if "jetson nano" in str(exec_shell(["cat", "/proc/device-tree/model"])).lower():
                return True
        
        return False
    
    @staticmethod
    def is_raspi():
        if SystemIdentity.is_linux():
            if "raspberry pi" in str(exec_shell(["cat", "/proc/device-tree/model"])).lower():
                return True
        
        return False
    
    @staticmethod
    def is_windows():
        if "windows" in platform.platform().lower():
            return True
        else:
            return False
    
    @staticmethod
    def is_linux():
        if "linux" in platform.platform().lower():
            return True
        else:
            return False
        
    @staticmethod
    def curr_board_model() -> Platform:
        if SystemIdentity.is_windows():
            return Platform.WINDOWS
        elif SystemIdentity.is_jetson_nano():
            return Platform.JETSON_NANO
        elif SystemIdentity.is_raspi():
            return Platform.RASPBERRY_PI

if __name__=="__main__":
    print(exec_shell(["cat", "/proc/device-tree/model"]))