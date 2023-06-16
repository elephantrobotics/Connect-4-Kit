# @author  : Zhu ZhenDong
# @time    : 2023-06-15 11-41-38
# @function: Program main entrance
# @version : 0.1


from typing import *
import sys

from PySide6.QtCore import Qt, QEvent, QObject, Signal, Slot
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
)
from layouts.app_page import AppPage
import assets.assets_rc


class MainWindow(QMainWindow):
    """App's MainWindow class

    Args:
        QMainWindow (_type_): _description_
    """

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.app_page = AppPage()
        self.app_page.setup_ui()

        self.setCentralWidget(self.app_page.get_widget())
        self.centralWidget().adjustSize()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    app.exec()
