from ArmCamera import ArmCamera
from Detection import ChessBoardDetector
from mouse_callbacks import *

# 创建相机对象
camera = ArmCamera(1)
# 创建棋盘检测器对象
detector = ChessBoardDetector(camera.mtx, camera.dist)

# 循环读取相机帧
while True:
    camera.update()
    frame = camera.get_frame()
    if frame is None:
        continue

    # 显示相机帧
    cv2.imshow("Main", frame)
    # 绑定鼠标事件
    bind_mouse_event(frame, "Main", mouseHSV)

    # 检测棋盘
    detector.detect(frame)
    if detector.is_grid_changed():
        # 显示棋盘信息
        detector.debug_display_chess_console()

    # 按q键退出循环
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# 关闭所有窗口
cv2.destroyAllWindows()
