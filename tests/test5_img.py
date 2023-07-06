import sys

sys.path.append("..")
print(sys.path)


from core.ArmCamera import ArmCamera
from core.Detection import ChessBoardDetector
from core.mouse_callbacks import *

# Create a camera object
camera = ArmCamera(1)
# Create a chessboard detector object
detector = ChessBoardDetector(camera.mtx, camera.dist)

# Continuously read frames from the camera
while True:
    camera.update()
    frame = camera.get_frame()
    if frame is None:
        continue

    # Display the camera frame
    cv2.imshow("Raw", frame)

    rec_frame = detector.rectify_frame(frame)
    if rec_frame is not None:
        cv2.imshow("Rectified frame", rec_frame)

    # Exit the loop if 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# Close all windows
cv2.destroyAllWindows()