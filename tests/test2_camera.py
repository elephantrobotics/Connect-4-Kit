# @author  : Zhu ZhenDong
# @time    : 2023-07-06 10-27-06
# @function:
# @version :

import cv2
import time

cam_index = 0
fps = 30

cap = cv2.VideoCapture(cam_index)

while True:
    ret, frame = cap.read()
    if not ret:
        continue

    cv2.imshow("Camera view", frame)

    if cv2.waitKey(1) == ord("q"):
        break

    time.sleep(1 / fps)

cv2.destroyAllWindows()
