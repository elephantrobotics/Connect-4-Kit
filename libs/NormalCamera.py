# Importing necessary libraries
import cv2
from libs.Camera import Camera
import numpy as np

# Defining the NormalCamera class which inherits from the Camera class
class NormalCamera(Camera):
    # Initializing the class with camera index, matrix and distortion parameters
    def __init__(self, cam_index=0, mtx=None, dist=None):
        super().__init__(mtx=mtx, dist=dist)
        self.cap = cv2.VideoCapture(cam_index)  # Capturing video from the camera

    # Method to get undistorted color frame
    def undistorted_color_frame(self) -> np.ndarray:
        frame = self.raw_color_frame()  # Getting raw color frame
        h, w = frame.shape[:2]  # Getting height and width of the frame
        # Getting optimal new camera matrix and region of interest
        new_camera_mtx, roi = cv2.getOptimalNewCameraMatrix(
            self.mtx, self.dist, (w, h), 1, (w, h)
        )
        # Undistorting the frame
        dst = cv2.undistort(frame, self.mtx, self.dist, None, new_camera_mtx)
        x, y, w, h = roi  # Getting region of interest parameters
        dst = dst[y : y + h, x : x + w]  # Cropping the frame to the region of interest
        return dst  # Returning the undistorted color frame

    # Method to get raw color frame
    def raw_color_frame(self) -> np.ndarray:
        _, frame = self.cap.read()  # Reading a frame from the video
        return frame  # Returning the raw color frame

    # Method to release the video capture
    def release(self):
        self.cap.release()  # Releasing the video capture

# Main function
if __name__ == "__main__":
    # Creating an instance of the NormalCamera class
    cam = NormalCamera()
    while True:
        frame = cam.raw_color_frame()  # Getting raw color frame
        print(frame.shape)  # Printing the shape of the frame
        window_name = "preview"  # Defining the window name
        cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)  # Creating a named window
        cv2.imshow(window_name, frame)  # Displaying the frame in the window
        # Breaking the loop if 'q' is pressed
        if cv2.waitKey(1) == ord("q"):
            break
