# Importing necessary libraries
import cv2
from functools import partial
from typing import *
import numpy as np

# Function to get RGB values and coordinates on mouse click
def mouseRGB(img: np.ndarray, event, x, y, flags, param):
    # Check if left button of mouse is clicked
    if event == cv2.EVENT_LBUTTONDOWN:
        # Get the Red, Green, Blue values of the pixel
        colorsR = img[y, x, 0]
        colorsG = img[y, x, 1]
        colorsB = img[y, x, 2]
        colors = img[y, x]
        # Print the Red, Green, Blue values and the coordinates of the pixel
        print("Red: ", colorsR) 
        print("Green: ", colorsG) 
        print("Blue: ", colorsB) 
        print("RGB Format: ", colors) 
        print("Coordinates of pixel: X: ", x, "Y: ", y) 

# Function to get HSV values and coordinates on mouse click
def mouseHSV(bgr_data, event, x, y, flags, param):
    # Check if left button of mouse is clicked
    if event == cv2.EVENT_LBUTTONDOWN:
        # Convert the BGR image to HSV
        bgr_data = cv2.cvtColor(bgr_data, cv2.COLOR_BGR2HSV)
        # Get the Hue, Saturation, Value of the pixel
        colorsH = bgr_data[y, x, 0]
        colorsS = bgr_data[y, x, 1]
        colorsV = bgr_data[y, x, 2]
        colors = bgr_data[y, x]
        # Print the Hue, Saturation, Value and the coordinates of the pixel
        print("H: ", colorsH) 
        print("S: ", colorsS) 
        print("V: ", colorsV) 
        print("HSV Format: ", colors) 
        print(f"HSV ratio Format: {colorsH/179},{colorsS/255},{colorsV/255}") 
        print(f"HSV standard Format:{colorsH/179*360},{colorsS/255},{colorsV/255}") 
        print("Coordinates of pixel: X: ", x, "Y: ", y) 

# List of supported mouse event functions
SUPPORTED_FUNC = [mouseRGB, mouseHSV]

# Function to bind mouse event to a window
def bind_mouse_event(img, window_name, func):
    # Check if the function is supported
    if func not in SUPPORTED_FUNC:
        print("Function not supported.")
        return
    # Create a partial function with the image as the first argument
    partial_click = partial(func, img)
    # Set the mouse callback function for the window
    cv2.setMouseCallback(window_name, partial_click)
