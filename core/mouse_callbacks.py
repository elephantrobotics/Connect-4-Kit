import cv2
from functools import partial
from typing import *
import numpy as np

# 鼠标点击事件，获取RGB值和坐标
def mouseRGB(img: np.ndarray, event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        colorsR = img[y, x, 0]
        colorsG = img[y, x, 1]
        colorsB = img[y, x, 2]
        colors = img[y, x]
        print("Red: ", colorsR) # 红色通道值
        print("Green: ", colorsG) # 绿色通道值
        print("Blue: ", colorsB) # 蓝色通道值
        print("RGB Format: ", colors) # RGB格式
        print("Coordinates of pixel: X: ", x, "Y: ", y) # 像素坐标

# 鼠标点击事件，获取HSV值和坐标
def mouseHSV(bgr_data, event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        bgr_data = cv2.cvtColor(bgr_data, cv2.COLOR_BGR2HSV)
        colorsH = bgr_data[y, x, 0]
        colorsS = bgr_data[y, x, 1]
        colorsV = bgr_data[y, x, 2]
        colors = bgr_data[y, x]
        print("H: ", colorsH) # 色调值
        print("S: ", colorsS) # 饱和度值
        print("V: ", colorsV) # 明度值
        print("HSV Format: ", colors) # HSV格式
        print(f"HSV ratio Format: {colorsH/179},{colorsS/255},{colorsV/255}") # HSV比例格式
        print(f"HSV standard Format:{colorsH/179*360},{colorsS/255},{colorsV/255}") # HSV标准格式
        print("Coordinates of pixel: X: ", x, "Y: ", y) # 像素坐标

# 支持的鼠标事件函数
SUPPORTED_FUNC = [mouseRGB, mouseHSV]

# 绑定鼠标事件
def bind_mouse_event(img, window_name, func):
    if func not in SUPPORTED_FUNC:
        print("Function not supported.")
        return

    partial_click = partial(func, img)
    cv2.setMouseCallback(window_name, partial_click)

