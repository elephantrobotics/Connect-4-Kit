import cv2
from libs.Camera import Camera
import numpy as np


class NormalCamera(Camera):
    def __init__(self, cam_index=0, mtx=None, dist=None):
        super().__init__(mtx=mtx, dist=dist)
        self.cap = cv2.VideoCapture(cam_index)

    def undistorted_color_frame(self) -> np.ndarray:
        frame = self.raw_color_frame()
        h, w = frame.shape[:2]
        new_camera_mtx, roi = cv2.getOptimalNewCameraMatrix(
            self.mtx, self.dist, (w, h), 1, (w, h)
        )
        dst = cv2.undistort(frame, self.mtx, self.dist, None, new_camera_mtx)
        x, y, w, h = roi
        dst = dst[y : y + h, x : x + w]
        return dst

    def raw_color_frame(self) -> np.ndarray:
        _, frame = self.cap.read()
        return frame

    def release(self):
        self.cap.release()


if __name__ == "__main__":
    # camera_params = np.load("../Configs/normal_cam_2_params.npz")
    # mtx, dist = camera_params["mtx"], camera_params["dist"]
    # cam = NormalCamera(mtx, dist)
    cam = NormalCamera()
    while True:
        frame = cam.raw_color_frame()
        print(frame.shape)
        window_name = "preview"
        cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
        # cv2.resizeWindow(window_name, 1280, 720)
        cv2.imshow(window_name, frame)
        if cv2.waitKey(1) == ord("q"):
            break
