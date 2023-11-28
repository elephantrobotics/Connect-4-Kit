import sys
import os
import time
from tkinter import NO

sys.path.append(os.getcwd())
from core.utils import SystemIdentity
from core.ArmCamera import ArmCamera
from core.Detection import ChessBoardDetector
from core.mouse_callbacks import *
from core.ArmInterface import _MyArm, _MyCobot
from tests.utils import select_com, select_robot_model
from libs.ArucoDetector import ArucoDetector
from pymycobot import MyCobot

robot_model = select_robot_model()
if SystemIdentity.is_jetson_nano():
    com = "/dev/ttyTHS1"
else:
    com = select_com()


arm = None
if robot_model == MyCobot:
    arm = _MyCobot(com)
else:
    arm = _MyArm(com)

arm.mc.send_angles(arm.angle_table["observe"], arm.ARM_SPEED)
camera_params = np.load("libs/normal_cam_params.npz")
mtx, dist = camera_params["mtx"], camera_params["dist"]
aruco_detector = ArucoDetector(mtx, dist, 20)

# change it in according to your case
cam_index = 0

# Create a camera object
camera = ArmCamera(cam_index)
# Create a chessboard detector object
detector = ChessBoardDetector(camera.mtx, camera.dist)

frame_count = 0
valid_count = 0
t = time.time()

# Continuously read frames from the camera
while True:
    frame_count += 1

    camera.update()
    frame = camera.get_frame()
    if frame is None:
        time.sleep(0.1)
        continue

    rec_frame = detector.rectify_frame(frame)
    if rec_frame is not None:
        valid_count += 1
        cv2.imshow("Rectified frame", rec_frame)

    corners, ids, rejectedImgPoints = aruco_detector.detect_marker_corners(frame)
    if len(corners) != 0:
        rvec, tvec = aruco_detector.estimatePoseSingleMarkers(corners)
        aruco_detector.draw_marker(frame, corners, tvec, rvec, ids)

    # Display the camera frame
    cv2.imshow("Raw", frame)

    # Exit the loop if 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break
    if time.time() - t > 1:
        t = time.time()
        print(f"Valid rate : {valid_count / frame_count}")
        frame_count = 0
        valid_count = 0

    time.sleep(0.1)

# Close all windows
cv2.destroyAllWindows()
