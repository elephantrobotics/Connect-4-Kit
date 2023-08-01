import sys
import os

sys.path.append(os.getcwd())

from core.ArmInterface import ArmInterface
import time

arm = ArmInterface("COM7", 115200)
arm.recovery()

i = 4  
arm.mc.send_angles(arm.chess_table[i], 50)
time.sleep(3)
for i in range(6):
    arm.drop_piece()
    time.sleep(1)
