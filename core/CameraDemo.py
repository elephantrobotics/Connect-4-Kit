from ArmCamera import ArmCamera
from Detection import ChessBoardDetector
from mouse_callbacks import *

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
    cv2.imshow("Main", frame)
    # Bind mouse events
    bind_mouse_event(frame, "Main", mouseHSV)

    # Detect the chessboard
    detector.detect(frame)
    if detector.is_grid_changed():
        # Display chessboard information
        detector.debug_display_chess_console()

    # Exit the loop if 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# Close all windows
cv2.destroyAllWindows()
