from typing import *
import sys
import logging
from core.logger import get_logger

from PySide6.QtCore import (
    QTranslator,
    QLocale,
)
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget
from PySide6.QtGui import QIcon

# Importing the layout of the application
from layouts.app_page import AppPage

# Importing the assets for the application
import assets.assets_rc


# Defining the main window class for the application
class MainWindow(QMainWindow):
    """App's MainWindow class

    Args:
        QMainWindow (_type_): _description_
    """
    
    # Initializer function for the MainWindow class
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        # Creating an instance of the AppPage class
        self.app_page = AppPage()
        # Setting up the UI for the app page
        self.app_page.setup_ui()

        # Setting the central widget for the main window
        self.setCentralWidget(self.app_page.get_widget())
        # Adjusting the size of the central widget
        self.centralWidget().adjustSize()


# Checking if the script is being run directly
if __name__ == "__main__":
    # set global logger to ignore most information
    # let child logger do specific job
    logging.getLogger().setLevel(logging.CRITICAL)

    logger = get_logger(__name__)
    logger.debug("Program Start.")

    trans = QTranslator()

    # Creating an instance of QApplication
    app = QApplication(sys.argv)

    path = "./assets/locales/"
    translator = QTranslator(app)

    if translator.load(path + QLocale.system().name()):
        logger.debug(QLocale.system().name() + " translation loaded.")

        # debug use : change to en temporarily
        translator.load(path + "en")
        app.installTranslator(translator)

    # Creating an instance of MainWindow
    main_window = MainWindow()
    # Displaying the main window
    main_window.setWindowTitle("Connect-4-Kit")
    main_window.setWindowIcon(QIcon("assets\icons\connect4-icon.png"))
    main_window.show()

    # Executing the application
    app.exec()
