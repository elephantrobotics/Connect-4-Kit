# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'app_page.ui'
##
## Created by: Qt User Interface Compiler version 6.5.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QFrame,
    QGridLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QSizePolicy, QSpacerItem, QVBoxLayout,
    QWidget)
import assets_rc

class Ui_AppPage(object):
    def setupUi(self, AppPage):
        if not AppPage.objectName():
            AppPage.setObjectName(u"AppPage")
        AppPage.resize(1096, 600)
        AppPage.setMinimumSize(QSize(1000, 600))
        AppPage.setStyleSheet(u"background : rgb(242, 243, 245)")
        self.horizontalLayout_13 = QHBoxLayout(AppPage)
        self.horizontalLayout_13.setObjectName(u"horizontalLayout_13")
        self.frame_interact_panel = QFrame(AppPage)
        self.frame_interact_panel.setObjectName(u"frame_interact_panel")
        self.frame_interact_panel.setStyleSheet(u"background : rgb(255, 255, 255)")
        self.verticalLayout_12 = QVBoxLayout(self.frame_interact_panel)
        self.verticalLayout_12.setObjectName(u"verticalLayout_12")
        self.layout_title = QHBoxLayout()
        self.layout_title.setObjectName(u"layout_title")
        self.layout_title.setContentsMargins(0, -1, -1, -1)
        self.label = QLabel(self.frame_interact_panel)
        self.label.setObjectName(u"label")
        sizePolicy = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setMinimumSize(QSize(0, 0))
        self.label.setMaximumSize(QSize(45, 32))
        self.label.setStyleSheet(u"font: 700 20pt \"Microsoft YaHei UI\";")
        self.label.setPixmap(QPixmap(u":/icons/icons/connect4-icon.png"))
        self.label.setScaledContents(True)

        self.layout_title.addWidget(self.label)

        self.label_2 = QLabel(self.frame_interact_panel)
        self.label_2.setObjectName(u"label_2")
        sizePolicy1 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy1)
        self.label_2.setStyleSheet(u"font: 700 10pt \"Microsoft YaHei UI\";")

        self.layout_title.addWidget(self.label_2, 0, Qt.AlignLeft)

        self.layout_title.setStretch(0, 1)
        self.layout_title.setStretch(1, 8)

        self.verticalLayout_12.addLayout(self.layout_title)

        self.label_separator = QLabel(self.frame_interact_panel)
        self.label_separator.setObjectName(u"label_separator")
        self.label_separator.setEnabled(True)
        sizePolicy2 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Maximum)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.label_separator.sizePolicy().hasHeightForWidth())
        self.label_separator.setSizePolicy(sizePolicy2)

        self.verticalLayout_12.addWidget(self.label_separator)

        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setSpacing(6)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.layout_cam_selection = QHBoxLayout()
        self.layout_cam_selection.setObjectName(u"layout_cam_selection")
        self.layout_cam_selection.setContentsMargins(0, -1, -1, -1)
        self.label_cam_icon = QLabel(self.frame_interact_panel)
        self.label_cam_icon.setObjectName(u"label_cam_icon")
        sizePolicy.setHeightForWidth(self.label_cam_icon.sizePolicy().hasHeightForWidth())
        self.label_cam_icon.setSizePolicy(sizePolicy)
        self.label_cam_icon.setMinimumSize(QSize(0, 0))

        self.layout_cam_selection.addWidget(self.label_cam_icon)

        self.label_camera_selection = QLabel(self.frame_interact_panel)
        self.label_camera_selection.setObjectName(u"label_camera_selection")
        self.label_camera_selection.setStyleSheet(u"font: 700 10pt \"Microsoft YaHei UI\";")
        self.label_camera_selection.setScaledContents(False)
        self.label_camera_selection.setWordWrap(False)

        self.layout_cam_selection.addWidget(self.label_camera_selection)

        self.label_3 = QLabel(self.frame_interact_panel)
        self.label_3.setObjectName(u"label_3")
        sizePolicy.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy)

        self.layout_cam_selection.addWidget(self.label_3)


        self.verticalLayout_4.addLayout(self.layout_cam_selection)

        self.combo_camera_selection = QComboBox(self.frame_interact_panel)
        self.combo_camera_selection.addItem("")
        self.combo_camera_selection.addItem("")
        self.combo_camera_selection.addItem("")
        self.combo_camera_selection.addItem("")
        self.combo_camera_selection.addItem("")
        self.combo_camera_selection.addItem("")
        self.combo_camera_selection.addItem("")
        self.combo_camera_selection.setObjectName(u"combo_camera_selection")
        sizePolicy3 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.combo_camera_selection.sizePolicy().hasHeightForWidth())
        self.combo_camera_selection.setSizePolicy(sizePolicy3)
        self.combo_camera_selection.setStyleSheet(u"border-radius:5px;\n"
"border:1px solid black;\n"
"border-style:outset;")

        self.verticalLayout_4.addWidget(self.combo_camera_selection)

        self.horizontalLayout_12 = QHBoxLayout()
        self.horizontalLayout_12.setObjectName(u"horizontalLayout_12")
        self.label_6 = QLabel(self.frame_interact_panel)
        self.label_6.setObjectName(u"label_6")
        sizePolicy4 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.label_6.sizePolicy().hasHeightForWidth())
        self.label_6.setSizePolicy(sizePolicy4)
        self.label_6.setStyleSheet(u"font: 700 9pt \"Microsoft YaHei UI\";")

        self.horizontalLayout_12.addWidget(self.label_6)

        self.switch_video0_on = QCheckBox(self.frame_interact_panel)
        self.switch_video0_on.setObjectName(u"switch_video0_on")
        sizePolicy5 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Preferred)
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(self.switch_video0_on.sizePolicy().hasHeightForWidth())
        self.switch_video0_on.setSizePolicy(sizePolicy5)

        self.horizontalLayout_12.addWidget(self.switch_video0_on)

        self.horizontalLayout_12.setStretch(0, 9)
        self.horizontalLayout_12.setStretch(1, 1)

        self.verticalLayout_4.addLayout(self.horizontalLayout_12)

        self.horizontalLayout_14 = QHBoxLayout()
        self.horizontalLayout_14.setObjectName(u"horizontalLayout_14")
        self.label_7 = QLabel(self.frame_interact_panel)
        self.label_7.setObjectName(u"label_7")
        sizePolicy4.setHeightForWidth(self.label_7.sizePolicy().hasHeightForWidth())
        self.label_7.setSizePolicy(sizePolicy4)
        self.label_7.setStyleSheet(u"font: 700 10pt \"Microsoft YaHei UI\";")

        self.horizontalLayout_14.addWidget(self.label_7)

        self.switch_video1_on = QCheckBox(self.frame_interact_panel)
        self.switch_video1_on.setObjectName(u"switch_video1_on")
        sizePolicy5.setHeightForWidth(self.switch_video1_on.sizePolicy().hasHeightForWidth())
        self.switch_video1_on.setSizePolicy(sizePolicy5)

        self.horizontalLayout_14.addWidget(self.switch_video1_on)

        self.horizontalLayout_14.setStretch(0, 9)
        self.horizontalLayout_14.setStretch(1, 1)

        self.verticalLayout_4.addLayout(self.horizontalLayout_14)

        self.horizontalLayout_15 = QHBoxLayout()
        self.horizontalLayout_15.setSpacing(1)
        self.horizontalLayout_15.setObjectName(u"horizontalLayout_15")
        self.btn_start_camera = QPushButton(self.frame_interact_panel)
        self.btn_start_camera.setObjectName(u"btn_start_camera")
        sizePolicy3.setHeightForWidth(self.btn_start_camera.sizePolicy().hasHeightForWidth())
        self.btn_start_camera.setSizePolicy(sizePolicy3)
        self.btn_start_camera.setStyleSheet(u"border-radius:5px;\n"
"border:1px solid black;\n"
"border-style:outset;")

        self.horizontalLayout_15.addWidget(self.btn_start_camera)

        self.btn_stop_camera = QPushButton(self.frame_interact_panel)
        self.btn_stop_camera.setObjectName(u"btn_stop_camera")
        sizePolicy3.setHeightForWidth(self.btn_stop_camera.sizePolicy().hasHeightForWidth())
        self.btn_stop_camera.setSizePolicy(sizePolicy3)
        self.btn_stop_camera.setStyleSheet(u"border-radius:5px;\n"
"border:1px solid black;\n"
"border-style:outset;")

        self.horizontalLayout_15.addWidget(self.btn_stop_camera)

        self.horizontalLayout_15.setStretch(0, 1)
        self.horizontalLayout_15.setStretch(1, 1)

        self.verticalLayout_4.addLayout(self.horizontalLayout_15)

        self.verticalLayout_4.setStretch(0, 1)
        self.verticalLayout_4.setStretch(1, 1)
        self.verticalLayout_4.setStretch(2, 1)
        self.verticalLayout_4.setStretch(3, 1)
        self.verticalLayout_4.setStretch(4, 1)

        self.verticalLayout_12.addLayout(self.verticalLayout_4)

        self.verticalLayout_5 = QVBoxLayout()
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.layout_algorithm_title = QHBoxLayout()
        self.layout_algorithm_title.setObjectName(u"layout_algorithm_title")
        self.layout_algorithm_title.setContentsMargins(0, -1, -1, -1)
        self.label_16 = QLabel(self.frame_interact_panel)
        self.label_16.setObjectName(u"label_16")
        sizePolicy.setHeightForWidth(self.label_16.sizePolicy().hasHeightForWidth())
        self.label_16.setSizePolicy(sizePolicy)

        self.layout_algorithm_title.addWidget(self.label_16)

        self.label_17 = QLabel(self.frame_interact_panel)
        self.label_17.setObjectName(u"label_17")
        self.label_17.setStyleSheet(u"font: 700 10pt \"Microsoft YaHei UI\";")

        self.layout_algorithm_title.addWidget(self.label_17)

        self.label_4 = QLabel(self.frame_interact_panel)
        self.label_4.setObjectName(u"label_4")
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)

        self.layout_algorithm_title.addWidget(self.label_4)

        self.layout_algorithm_title.setStretch(0, 1)
        self.layout_algorithm_title.setStretch(1, 8)

        self.verticalLayout_5.addLayout(self.layout_algorithm_title)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setSpacing(1)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.pushButton_9 = QPushButton(self.frame_interact_panel)
        self.pushButton_9.setObjectName(u"pushButton_9")
        sizePolicy3.setHeightForWidth(self.pushButton_9.sizePolicy().hasHeightForWidth())
        self.pushButton_9.setSizePolicy(sizePolicy3)
        self.pushButton_9.setStyleSheet(u"border-radius:5px;\n"
"border:1px solid black;\n"
"border-style:outset;")

        self.horizontalLayout_2.addWidget(self.pushButton_9)

        self.pushButton_10 = QPushButton(self.frame_interact_panel)
        self.pushButton_10.setObjectName(u"pushButton_10")
        sizePolicy3.setHeightForWidth(self.pushButton_10.sizePolicy().hasHeightForWidth())
        self.pushButton_10.setSizePolicy(sizePolicy3)
        self.pushButton_10.setStyleSheet(u"border-radius:5px;\n"
"border:1px solid black;\n"
"border-style:outset;")

        self.horizontalLayout_2.addWidget(self.pushButton_10)

        self.horizontalLayout_2.setStretch(0, 1)
        self.horizontalLayout_2.setStretch(1, 1)

        self.verticalLayout_5.addLayout(self.horizontalLayout_2)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label_18 = QLabel(self.frame_interact_panel)
        self.label_18.setObjectName(u"label_18")
        sizePolicy4.setHeightForWidth(self.label_18.sizePolicy().hasHeightForWidth())
        self.label_18.setSizePolicy(sizePolicy4)

        self.horizontalLayout.addWidget(self.label_18)

        self.combo_algs = QComboBox(self.frame_interact_panel)
        self.combo_algs.setObjectName(u"combo_algs")
        sizePolicy3.setHeightForWidth(self.combo_algs.sizePolicy().hasHeightForWidth())
        self.combo_algs.setSizePolicy(sizePolicy3)
        self.combo_algs.setStyleSheet(u"border-radius:5px;\n"
"border:1px solid black;\n"
"border-style:outset;")

        self.horizontalLayout.addWidget(self.combo_algs)


        self.verticalLayout_5.addLayout(self.horizontalLayout)

        self.verticalLayout_5.setStretch(0, 1)
        self.verticalLayout_5.setStretch(1, 1)
        self.verticalLayout_5.setStretch(2, 1)

        self.verticalLayout_12.addLayout(self.verticalLayout_5)

        self.verticalLayout_11 = QVBoxLayout()
        self.verticalLayout_11.setObjectName(u"verticalLayout_11")
        self.layout_algorithm_title_2 = QHBoxLayout()
        self.layout_algorithm_title_2.setObjectName(u"layout_algorithm_title_2")
        self.layout_algorithm_title_2.setContentsMargins(0, -1, -1, -1)
        self.label_21 = QLabel(self.frame_interact_panel)
        self.label_21.setObjectName(u"label_21")
        sizePolicy.setHeightForWidth(self.label_21.sizePolicy().hasHeightForWidth())
        self.label_21.setSizePolicy(sizePolicy)

        self.layout_algorithm_title_2.addWidget(self.label_21)

        self.label_22 = QLabel(self.frame_interact_panel)
        self.label_22.setObjectName(u"label_22")
        self.label_22.setStyleSheet(u"font: 700 10pt \"Microsoft YaHei UI\";")

        self.layout_algorithm_title_2.addWidget(self.label_22)

        self.label_23 = QLabel(self.frame_interact_panel)
        self.label_23.setObjectName(u"label_23")
        sizePolicy.setHeightForWidth(self.label_23.sizePolicy().hasHeightForWidth())
        self.label_23.setSizePolicy(sizePolicy)

        self.layout_algorithm_title_2.addWidget(self.label_23)

        self.layout_algorithm_title_2.setStretch(0, 1)
        self.layout_algorithm_title_2.setStretch(1, 8)

        self.verticalLayout_11.addLayout(self.layout_algorithm_title_2)

        self.horizontalLayout_10 = QHBoxLayout()
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.label_24 = QLabel(self.frame_interact_panel)
        self.label_24.setObjectName(u"label_24")
        sizePolicy4.setHeightForWidth(self.label_24.sizePolicy().hasHeightForWidth())
        self.label_24.setSizePolicy(sizePolicy4)
        self.label_24.setStyleSheet(u"font: 700 9pt \"Microsoft YaHei UI\";")

        self.horizontalLayout_10.addWidget(self.label_24)

        self.checkBox = QCheckBox(self.frame_interact_panel)
        self.checkBox.setObjectName(u"checkBox")
        sizePolicy3.setHeightForWidth(self.checkBox.sizePolicy().hasHeightForWidth())
        self.checkBox.setSizePolicy(sizePolicy3)

        self.horizontalLayout_10.addWidget(self.checkBox)

        self.horizontalLayout_10.setStretch(0, 9)
        self.horizontalLayout_10.setStretch(1, 1)

        self.verticalLayout_11.addLayout(self.horizontalLayout_10)

        self.horizontalLayout_11 = QHBoxLayout()
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.label_25 = QLabel(self.frame_interact_panel)
        self.label_25.setObjectName(u"label_25")
        sizePolicy4.setHeightForWidth(self.label_25.sizePolicy().hasHeightForWidth())
        self.label_25.setSizePolicy(sizePolicy4)
        self.label_25.setStyleSheet(u"font: 700 9pt \"Microsoft YaHei UI\";")

        self.horizontalLayout_11.addWidget(self.label_25)

        self.lineEdit = QLineEdit(self.frame_interact_panel)
        self.lineEdit.setObjectName(u"lineEdit")
        sizePolicy6 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        sizePolicy6.setHorizontalStretch(0)
        sizePolicy6.setVerticalStretch(0)
        sizePolicy6.setHeightForWidth(self.lineEdit.sizePolicy().hasHeightForWidth())
        self.lineEdit.setSizePolicy(sizePolicy6)

        self.horizontalLayout_11.addWidget(self.lineEdit)

        self.horizontalLayout_11.setStretch(0, 8)
        self.horizontalLayout_11.setStretch(1, 2)

        self.verticalLayout_11.addLayout(self.horizontalLayout_11)

        self.horizontalLayout_19 = QHBoxLayout()
        self.horizontalLayout_19.setObjectName(u"horizontalLayout_19")
        self.label_26 = QLabel(self.frame_interact_panel)
        self.label_26.setObjectName(u"label_26")
        sizePolicy4.setHeightForWidth(self.label_26.sizePolicy().hasHeightForWidth())
        self.label_26.setSizePolicy(sizePolicy4)
        self.label_26.setStyleSheet(u"font: 700 9pt \"Microsoft YaHei UI\";")

        self.horizontalLayout_19.addWidget(self.label_26)

        self.lineEdit_2 = QLineEdit(self.frame_interact_panel)
        self.lineEdit_2.setObjectName(u"lineEdit_2")
        sizePolicy6.setHeightForWidth(self.lineEdit_2.sizePolicy().hasHeightForWidth())
        self.lineEdit_2.setSizePolicy(sizePolicy6)

        self.horizontalLayout_19.addWidget(self.lineEdit_2)

        self.horizontalLayout_19.setStretch(0, 8)
        self.horizontalLayout_19.setStretch(1, 2)

        self.verticalLayout_11.addLayout(self.horizontalLayout_19)


        self.verticalLayout_12.addLayout(self.verticalLayout_11)

        self.verticalLayout_9 = QVBoxLayout()
        self.verticalLayout_9.setSpacing(6)
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.horizontalLayout_16 = QHBoxLayout()
        self.horizontalLayout_16.setObjectName(u"horizontalLayout_16")
        self.label_8 = QLabel(self.frame_interact_panel)
        self.label_8.setObjectName(u"label_8")
        sizePolicy4.setHeightForWidth(self.label_8.sizePolicy().hasHeightForWidth())
        self.label_8.setSizePolicy(sizePolicy4)
        self.label_8.setStyleSheet(u"font: 700 9pt \"Microsoft YaHei UI\";")

        self.horizontalLayout_16.addWidget(self.label_8)

        self.switch_video2_on = QCheckBox(self.frame_interact_panel)
        self.switch_video2_on.setObjectName(u"switch_video2_on")
        sizePolicy3.setHeightForWidth(self.switch_video2_on.sizePolicy().hasHeightForWidth())
        self.switch_video2_on.setSizePolicy(sizePolicy3)

        self.horizontalLayout_16.addWidget(self.switch_video2_on)

        self.horizontalLayout_16.setStretch(0, 9)
        self.horizontalLayout_16.setStretch(1, 1)

        self.verticalLayout_9.addLayout(self.horizontalLayout_16)

        self.horizontalLayout_17 = QHBoxLayout()
        self.horizontalLayout_17.setObjectName(u"horizontalLayout_17")
        self.label_14 = QLabel(self.frame_interact_panel)
        self.label_14.setObjectName(u"label_14")
        sizePolicy4.setHeightForWidth(self.label_14.sizePolicy().hasHeightForWidth())
        self.label_14.setSizePolicy(sizePolicy4)
        self.label_14.setStyleSheet(u"font: 700 9pt \"Microsoft YaHei UI\";")

        self.horizontalLayout_17.addWidget(self.label_14)

        self.switch_video3_on = QCheckBox(self.frame_interact_panel)
        self.switch_video3_on.setObjectName(u"switch_video3_on")
        sizePolicy3.setHeightForWidth(self.switch_video3_on.sizePolicy().hasHeightForWidth())
        self.switch_video3_on.setSizePolicy(sizePolicy3)

        self.horizontalLayout_17.addWidget(self.switch_video3_on)

        self.horizontalLayout_17.setStretch(0, 9)
        self.horizontalLayout_17.setStretch(1, 1)

        self.verticalLayout_9.addLayout(self.horizontalLayout_17)

        self.verticalLayout_9.setStretch(0, 1)
        self.verticalLayout_9.setStretch(1, 1)

        self.verticalLayout_12.addLayout(self.verticalLayout_9)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_12.addItem(self.verticalSpacer_2)

        self.verticalLayout_12.setStretch(0, 1)
        self.verticalLayout_12.setStretch(1, 1)
        self.verticalLayout_12.setStretch(2, 5)
        self.verticalLayout_12.setStretch(3, 3)
        self.verticalLayout_12.setStretch(4, 4)
        self.verticalLayout_12.setStretch(5, 2)
        self.verticalLayout_12.setStretch(6, 4)

        self.horizontalLayout_13.addWidget(self.frame_interact_panel)

        self.frame_video = QFrame(AppPage)
        self.frame_video.setObjectName(u"frame_video")
        self.frame_video.setEnabled(True)
        sizePolicy3.setHeightForWidth(self.frame_video.sizePolicy().hasHeightForWidth())
        self.frame_video.setSizePolicy(sizePolicy3)
        self.frame_video.setStyleSheet(u"background : rgb(242, 243, 245)")
        self.frame_video.setFrameShape(QFrame.StyledPanel)
        self.frame_video.setFrameShadow(QFrame.Raised)
        self.verticalLayout_10 = QVBoxLayout(self.frame_video)
        self.verticalLayout_10.setSpacing(0)
        self.verticalLayout_10.setObjectName(u"verticalLayout_10")
        self.verticalLayout_10.setContentsMargins(10, 40, 10, 10)
        self.frame_8 = QFrame(self.frame_video)
        self.frame_8.setObjectName(u"frame_8")
        self.frame_8.setStyleSheet(u"background : rgb(255, 255, 255)")
        self.frame_8.setFrameShape(QFrame.StyledPanel)
        self.frame_8.setFrameShadow(QFrame.Raised)
        self.gridLayout = QGridLayout(self.frame_8)
        self.gridLayout.setObjectName(u"gridLayout")
        self.verticalLayout_13 = QVBoxLayout()
        self.verticalLayout_13.setObjectName(u"verticalLayout_13")
        self.label_27 = QLabel(self.frame_8)
        self.label_27.setObjectName(u"label_27")
        sizePolicy.setHeightForWidth(self.label_27.sizePolicy().hasHeightForWidth())
        self.label_27.setSizePolicy(sizePolicy)

        self.verticalLayout_13.addWidget(self.label_27)

        self.label_video_feed0 = QLabel(self.frame_8)
        self.label_video_feed0.setObjectName(u"label_video_feed0")
        sizePolicy7 = QSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        sizePolicy7.setHorizontalStretch(0)
        sizePolicy7.setVerticalStretch(0)
        sizePolicy7.setHeightForWidth(self.label_video_feed0.sizePolicy().hasHeightForWidth())
        self.label_video_feed0.setSizePolicy(sizePolicy7)
        self.label_video_feed0.setMinimumSize(QSize(0, 0))
        self.label_video_feed0.setStyleSheet(u"border:1px solid rgb(0, 255, 0);")
        self.label_video_feed0.setScaledContents(False)
        self.label_video_feed0.setMargin(0)

        self.verticalLayout_13.addWidget(self.label_video_feed0)


        self.gridLayout.addLayout(self.verticalLayout_13, 0, 0, 1, 1)

        self.verticalLayout_14 = QVBoxLayout()
        self.verticalLayout_14.setObjectName(u"verticalLayout_14")
        self.label_28 = QLabel(self.frame_8)
        self.label_28.setObjectName(u"label_28")
        sizePolicy.setHeightForWidth(self.label_28.sizePolicy().hasHeightForWidth())
        self.label_28.setSizePolicy(sizePolicy)

        self.verticalLayout_14.addWidget(self.label_28)

        self.label_video_feed1 = QLabel(self.frame_8)
        self.label_video_feed1.setObjectName(u"label_video_feed1")
        sizePolicy7.setHeightForWidth(self.label_video_feed1.sizePolicy().hasHeightForWidth())
        self.label_video_feed1.setSizePolicy(sizePolicy7)
        self.label_video_feed1.setStyleSheet(u"border:1px solid rgb(0, 255, 0);")
        self.label_video_feed1.setScaledContents(False)

        self.verticalLayout_14.addWidget(self.label_video_feed1)


        self.gridLayout.addLayout(self.verticalLayout_14, 0, 1, 1, 1)

        self.verticalLayout_16 = QVBoxLayout()
        self.verticalLayout_16.setObjectName(u"verticalLayout_16")
        self.label_29 = QLabel(self.frame_8)
        self.label_29.setObjectName(u"label_29")
        sizePolicy.setHeightForWidth(self.label_29.sizePolicy().hasHeightForWidth())
        self.label_29.setSizePolicy(sizePolicy)

        self.verticalLayout_16.addWidget(self.label_29)

        self.label_video_feed2 = QLabel(self.frame_8)
        self.label_video_feed2.setObjectName(u"label_video_feed2")
        sizePolicy7.setHeightForWidth(self.label_video_feed2.sizePolicy().hasHeightForWidth())
        self.label_video_feed2.setSizePolicy(sizePolicy7)
        self.label_video_feed2.setStyleSheet(u"border:1px solid rgb(0, 255, 0);")
        self.label_video_feed2.setScaledContents(False)

        self.verticalLayout_16.addWidget(self.label_video_feed2)


        self.gridLayout.addLayout(self.verticalLayout_16, 1, 0, 1, 1)

        self.verticalLayout_15 = QVBoxLayout()
        self.verticalLayout_15.setObjectName(u"verticalLayout_15")
        self.label_30 = QLabel(self.frame_8)
        self.label_30.setObjectName(u"label_30")
        sizePolicy.setHeightForWidth(self.label_30.sizePolicy().hasHeightForWidth())
        self.label_30.setSizePolicy(sizePolicy)

        self.verticalLayout_15.addWidget(self.label_30)

        self.label_video_feed3 = QLabel(self.frame_8)
        self.label_video_feed3.setObjectName(u"label_video_feed3")
        sizePolicy7.setHeightForWidth(self.label_video_feed3.sizePolicy().hasHeightForWidth())
        self.label_video_feed3.setSizePolicy(sizePolicy7)
        self.label_video_feed3.setStyleSheet(u"border:1px solid rgb(0, 255, 0);")
        self.label_video_feed3.setScaledContents(False)

        self.verticalLayout_15.addWidget(self.label_video_feed3)


        self.gridLayout.addLayout(self.verticalLayout_15, 1, 1, 1, 1)


        self.verticalLayout_10.addWidget(self.frame_8)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_10.addItem(self.verticalSpacer)

        self.verticalLayout_10.setStretch(0, 9)
        self.verticalLayout_10.setStretch(1, 1)

        self.horizontalLayout_13.addWidget(self.frame_video)

        self.frame_arm_control = QFrame(AppPage)
        self.frame_arm_control.setObjectName(u"frame_arm_control")
        self.frame_arm_control.setStyleSheet(u"background : rgb(242, 243, 245)")
        self.frame_arm_control.setFrameShape(QFrame.StyledPanel)
        self.frame_arm_control.setFrameShadow(QFrame.Raised)
        self.verticalLayout = QVBoxLayout(self.frame_arm_control)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(10, 0, 9, 10)
        self.horizontalLayout_18 = QHBoxLayout()
        self.horizontalLayout_18.setObjectName(u"horizontalLayout_18")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_18.addItem(self.horizontalSpacer)

        self.btn_back = QPushButton(self.frame_arm_control)
        self.btn_back.setObjectName(u"btn_back")
        sizePolicy8 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy8.setHorizontalStretch(0)
        sizePolicy8.setVerticalStretch(0)
        sizePolicy8.setHeightForWidth(self.btn_back.sizePolicy().hasHeightForWidth())
        self.btn_back.setSizePolicy(sizePolicy8)
        self.btn_back.setMinimumSize(QSize(32, 32))

        self.horizontalLayout_18.addWidget(self.btn_back)


        self.verticalLayout.addLayout(self.horizontalLayout_18)

        self.frame_10 = QFrame(self.frame_arm_control)
        self.frame_10.setObjectName(u"frame_10")
        self.frame_10.setStyleSheet(u"")
        self.frame_10.setFrameShape(QFrame.StyledPanel)
        self.frame_10.setFrameShadow(QFrame.Raised)
        self.verticalLayout_8 = QVBoxLayout(self.frame_10)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.verticalLayout_6 = QVBoxLayout()
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.label_5 = QLabel(self.frame_10)
        self.label_5.setObjectName(u"label_5")
        sizePolicy.setHeightForWidth(self.label_5.sizePolicy().hasHeightForWidth())
        self.label_5.setSizePolicy(sizePolicy)

        self.horizontalLayout_5.addWidget(self.label_5)

        self.label_9 = QLabel(self.frame_10)
        self.label_9.setObjectName(u"label_9")
        self.label_9.setStyleSheet(u"font: 700 10pt \"Microsoft YaHei UI\";")

        self.horizontalLayout_5.addWidget(self.label_9)

        self.label_20 = QLabel(self.frame_10)
        self.label_20.setObjectName(u"label_20")
        sizePolicy.setHeightForWidth(self.label_20.sizePolicy().hasHeightForWidth())
        self.label_20.setSizePolicy(sizePolicy)

        self.horizontalLayout_5.addWidget(self.label_20)

        self.horizontalLayout_5.setStretch(0, 1)
        self.horizontalLayout_5.setStretch(1, 9)
        self.horizontalLayout_5.setStretch(2, 1)

        self.verticalLayout_6.addLayout(self.horizontalLayout_5)

        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setSpacing(1)
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.pushButton_3 = QPushButton(self.frame_10)
        self.pushButton_3.setObjectName(u"pushButton_3")
        sizePolicy3.setHeightForWidth(self.pushButton_3.sizePolicy().hasHeightForWidth())
        self.pushButton_3.setSizePolicy(sizePolicy3)
        self.pushButton_3.setStyleSheet(u"border-radius:5px;\n"
"border:1px solid black;\n"
"border-style:outset;")

        self.horizontalLayout_7.addWidget(self.pushButton_3)

        self.pushButton_4 = QPushButton(self.frame_10)
        self.pushButton_4.setObjectName(u"pushButton_4")
        sizePolicy3.setHeightForWidth(self.pushButton_4.sizePolicy().hasHeightForWidth())
        self.pushButton_4.setSizePolicy(sizePolicy3)
        self.pushButton_4.setStyleSheet(u"border-radius:5px;\n"
"border:1px solid black;\n"
"border-style:outset;")

        self.horizontalLayout_7.addWidget(self.pushButton_4)


        self.verticalLayout_6.addLayout(self.horizontalLayout_7)


        self.verticalLayout_8.addLayout(self.verticalLayout_6)

        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.label_10 = QLabel(self.frame_10)
        self.label_10.setObjectName(u"label_10")
        sizePolicy.setHeightForWidth(self.label_10.sizePolicy().hasHeightForWidth())
        self.label_10.setSizePolicy(sizePolicy)

        self.horizontalLayout_4.addWidget(self.label_10)

        self.label_11 = QLabel(self.frame_10)
        self.label_11.setObjectName(u"label_11")
        self.label_11.setStyleSheet(u"font: 700 10pt \"Microsoft YaHei UI\";")

        self.horizontalLayout_4.addWidget(self.label_11)

        self.label_19 = QLabel(self.frame_10)
        self.label_19.setObjectName(u"label_19")
        sizePolicy.setHeightForWidth(self.label_19.sizePolicy().hasHeightForWidth())
        self.label_19.setSizePolicy(sizePolicy)

        self.horizontalLayout_4.addWidget(self.label_19)


        self.verticalLayout_3.addLayout(self.horizontalLayout_4)

        self.comboBox = QComboBox(self.frame_10)
        self.comboBox.setObjectName(u"comboBox")
        sizePolicy3.setHeightForWidth(self.comboBox.sizePolicy().hasHeightForWidth())
        self.comboBox.setSizePolicy(sizePolicy3)
        self.comboBox.setStyleSheet(u"border-radius:5px;\n"
"border:1px solid black;\n"
"border-style:outset;")

        self.verticalLayout_3.addWidget(self.comboBox)

        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setSpacing(1)
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.pushButton_5 = QPushButton(self.frame_10)
        self.pushButton_5.setObjectName(u"pushButton_5")
        sizePolicy3.setHeightForWidth(self.pushButton_5.sizePolicy().hasHeightForWidth())
        self.pushButton_5.setSizePolicy(sizePolicy3)
        self.pushButton_5.setStyleSheet(u"border-radius:5px;\n"
"border:1px solid black;\n"
"border-style:outset;")

        self.horizontalLayout_8.addWidget(self.pushButton_5)

        self.pushButton_6 = QPushButton(self.frame_10)
        self.pushButton_6.setObjectName(u"pushButton_6")
        sizePolicy3.setHeightForWidth(self.pushButton_6.sizePolicy().hasHeightForWidth())
        self.pushButton_6.setSizePolicy(sizePolicy3)
        self.pushButton_6.setStyleSheet(u"border-radius:5px;\n"
"border:1px solid black;\n"
"border-style:outset;")

        self.horizontalLayout_8.addWidget(self.pushButton_6)


        self.verticalLayout_3.addLayout(self.horizontalLayout_8)

        self.horizontalLayout_9 = QHBoxLayout()
        self.horizontalLayout_9.setSpacing(1)
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.pushButton_7 = QPushButton(self.frame_10)
        self.pushButton_7.setObjectName(u"pushButton_7")
        sizePolicy3.setHeightForWidth(self.pushButton_7.sizePolicy().hasHeightForWidth())
        self.pushButton_7.setSizePolicy(sizePolicy3)
        self.pushButton_7.setStyleSheet(u"border-radius:5px;\n"
"border:1px solid black;\n"
"border-style:outset;")

        self.horizontalLayout_9.addWidget(self.pushButton_7)

        self.pushButton_8 = QPushButton(self.frame_10)
        self.pushButton_8.setObjectName(u"pushButton_8")
        sizePolicy3.setHeightForWidth(self.pushButton_8.sizePolicy().hasHeightForWidth())
        self.pushButton_8.setSizePolicy(sizePolicy3)
        self.pushButton_8.setStyleSheet(u"border-radius:5px;\n"
"border:1px solid black;\n"
"border-style:outset;")

        self.horizontalLayout_9.addWidget(self.pushButton_8)


        self.verticalLayout_3.addLayout(self.horizontalLayout_9)


        self.verticalLayout_8.addLayout(self.verticalLayout_3)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.label_12 = QLabel(self.frame_10)
        self.label_12.setObjectName(u"label_12")
        sizePolicy.setHeightForWidth(self.label_12.sizePolicy().hasHeightForWidth())
        self.label_12.setSizePolicy(sizePolicy)

        self.horizontalLayout_3.addWidget(self.label_12)

        self.label_13 = QLabel(self.frame_10)
        self.label_13.setObjectName(u"label_13")
        self.label_13.setStyleSheet(u"font: 700 10pt \"Microsoft YaHei UI\";")

        self.horizontalLayout_3.addWidget(self.label_13)

        self.label_15 = QLabel(self.frame_10)
        self.label_15.setObjectName(u"label_15")
        sizePolicy.setHeightForWidth(self.label_15.sizePolicy().hasHeightForWidth())
        self.label_15.setSizePolicy(sizePolicy)

        self.horizontalLayout_3.addWidget(self.label_15)


        self.verticalLayout_2.addLayout(self.horizontalLayout_3)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setSpacing(1)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.pushButton = QPushButton(self.frame_10)
        self.pushButton.setObjectName(u"pushButton")
        sizePolicy3.setHeightForWidth(self.pushButton.sizePolicy().hasHeightForWidth())
        self.pushButton.setSizePolicy(sizePolicy3)
        self.pushButton.setStyleSheet(u"border-radius:5px;\n"
"border:1px solid black;\n"
"border-style:outset;")

        self.horizontalLayout_6.addWidget(self.pushButton)

        self.pushButton_2 = QPushButton(self.frame_10)
        self.pushButton_2.setObjectName(u"pushButton_2")
        sizePolicy3.setHeightForWidth(self.pushButton_2.sizePolicy().hasHeightForWidth())
        self.pushButton_2.setSizePolicy(sizePolicy3)
        self.pushButton_2.setStyleSheet(u"border-radius:5px;\n"
"border:1px solid black;\n"
"border-style:outset;")

        self.horizontalLayout_6.addWidget(self.pushButton_2)


        self.verticalLayout_2.addLayout(self.horizontalLayout_6)


        self.verticalLayout_8.addLayout(self.verticalLayout_2)

        self.verticalSpacer_3 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_8.addItem(self.verticalSpacer_3)

        self.verticalLayout_7 = QVBoxLayout()
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.btn_start_game = QPushButton(self.frame_10)
        self.btn_start_game.setObjectName(u"btn_start_game")
        sizePolicy3.setHeightForWidth(self.btn_start_game.sizePolicy().hasHeightForWidth())
        self.btn_start_game.setSizePolicy(sizePolicy3)
        self.btn_start_game.setStyleSheet(u"background: rgb(18, 147, 211);\n"
"color: rgb(255,255,255);\n"
"border-radius:10px;\n"
"border-style:outset;")

        self.verticalLayout_7.addWidget(self.btn_start_game)

        self.btn_stop_game = QPushButton(self.frame_10)
        self.btn_stop_game.setObjectName(u"btn_stop_game")
        sizePolicy3.setHeightForWidth(self.btn_stop_game.sizePolicy().hasHeightForWidth())
        self.btn_stop_game.setSizePolicy(sizePolicy3)
        self.btn_stop_game.setStyleSheet(u"background: rgb(221, 83, 52);\n"
"color: rgb(255,255,255);\n"
"border-radius:10px;\n"
"border-style:outset;")

        self.verticalLayout_7.addWidget(self.btn_stop_game)


        self.verticalLayout_8.addLayout(self.verticalLayout_7)

        self.verticalLayout_8.setStretch(0, 2)
        self.verticalLayout_8.setStretch(1, 4)
        self.verticalLayout_8.setStretch(2, 2)
        self.verticalLayout_8.setStretch(3, 6)
        self.verticalLayout_8.setStretch(4, 4)

        self.verticalLayout.addWidget(self.frame_10)

        self.verticalLayout.setStretch(0, 1)
        self.verticalLayout.setStretch(1, 7)

        self.horizontalLayout_13.addWidget(self.frame_arm_control)

        self.horizontalLayout_13.setStretch(0, 2)
        self.horizontalLayout_13.setStretch(1, 7)
        self.horizontalLayout_13.setStretch(2, 2)

        self.retranslateUi(AppPage)

        self.combo_camera_selection.setCurrentIndex(-1)


        QMetaObject.connectSlotsByName(AppPage)
    # setupUi

    def retranslateUi(self, AppPage):
        AppPage.setWindowTitle(QCoreApplication.translate("AppPage", u"Form", None))
        self.label.setText("")
        self.label_2.setText(QCoreApplication.translate("AppPage", u"\u56db\u5b50\u68cb\u5957\u88c5", None))
        self.label_separator.setText(QCoreApplication.translate("AppPage", u"\u5206\u5272\u7ebf", None))
        self.label_cam_icon.setText(QCoreApplication.translate("AppPage", u"X", None))
        self.label_camera_selection.setText(QCoreApplication.translate("AppPage", u"\u76f8\u673a\u9009\u62e9", None))
        self.label_3.setText(QCoreApplication.translate("AppPage", u"X", None))
        self.combo_camera_selection.setItemText(0, QCoreApplication.translate("AppPage", u"0", None))
        self.combo_camera_selection.setItemText(1, QCoreApplication.translate("AppPage", u"1", None))
        self.combo_camera_selection.setItemText(2, QCoreApplication.translate("AppPage", u"2", None))
        self.combo_camera_selection.setItemText(3, QCoreApplication.translate("AppPage", u"3", None))
        self.combo_camera_selection.setItemText(4, QCoreApplication.translate("AppPage", u"4", None))
        self.combo_camera_selection.setItemText(5, QCoreApplication.translate("AppPage", u"5", None))
        self.combo_camera_selection.setItemText(6, QCoreApplication.translate("AppPage", u"6", None))

        self.label_6.setText(QCoreApplication.translate("AppPage", u"\u9ed8\u8ba4\u89c6\u9891\u6d41", None))
        self.switch_video0_on.setText("")
        self.label_7.setText(QCoreApplication.translate("AppPage", u"\u7070\u5ea6\u6d41", None))
        self.switch_video1_on.setText("")
        self.btn_start_camera.setText(QCoreApplication.translate("AppPage", u"\u542f\u52a8", None))
        self.btn_stop_camera.setText(QCoreApplication.translate("AppPage", u"\u505c\u6b62", None))
        self.label_16.setText(QCoreApplication.translate("AppPage", u"X", None))
        self.label_17.setText(QCoreApplication.translate("AppPage", u"\u5bf9\u5f08\u6a21\u578b\u9009\u62e9", None))
        self.label_4.setText(QCoreApplication.translate("AppPage", u"X", None))
        self.pushButton_9.setText(QCoreApplication.translate("AppPage", u"\u5b98\u65b9\u6a21\u578b", None))
        self.pushButton_10.setText(QCoreApplication.translate("AppPage", u"\u81ea\u5b9a\u4e49\u6a21\u578b", None))
        self.label_18.setText(QCoreApplication.translate("AppPage", u"\u6a21\u578b", None))
        self.label_21.setText(QCoreApplication.translate("AppPage", u"X", None))
        self.label_22.setText(QCoreApplication.translate("AppPage", u"\u8bbe\u5b9a\u5bf9\u5f08\u89c4\u5219", None))
        self.label_23.setText(QCoreApplication.translate("AppPage", u"X", None))
        self.label_24.setText(QCoreApplication.translate("AppPage", u"\u673a\u5668\u4eba\u5148\u624b", None))
        self.checkBox.setText("")
        self.label_25.setText(QCoreApplication.translate("AppPage", u"\u5bf9\u5f08\u7b49\u5f85(\u79d2)", None))
        self.label_26.setText(QCoreApplication.translate("AppPage", u"\u7b49\u5f85\u6b21\u6570\u9650\u5236", None))
        self.label_8.setText(QCoreApplication.translate("AppPage", u"\u8bc6\u522b\u6807\u6ce8\u89c6\u9891\u6d41", None))
        self.switch_video2_on.setText("")
        self.label_14.setText(QCoreApplication.translate("AppPage", u"\u7b97\u6cd5\u7ed3\u679c\u5c55\u793a", None))
        self.switch_video3_on.setText("")
        self.label_27.setText(QCoreApplication.translate("AppPage", u"\u9ed8\u8ba4\u89c6\u9891\u6d41", None))
        self.label_video_feed0.setText(QCoreApplication.translate("AppPage", u"Video0", None))
        self.label_28.setText(QCoreApplication.translate("AppPage", u"\u7070\u5ea6\u89c6\u9891\u6d41", None))
        self.label_video_feed1.setText(QCoreApplication.translate("AppPage", u"Video1", None))
        self.label_29.setText(QCoreApplication.translate("AppPage", u"\u8bc6\u522b\u6807\u6ce8\u89c6\u9891\u6d41", None))
        self.label_video_feed2.setText(QCoreApplication.translate("AppPage", u"Video2", None))
        self.label_30.setText(QCoreApplication.translate("AppPage", u"\u7b97\u6cd5\u7ed3\u679c\u5c55\u793a", None))
        self.label_video_feed3.setText(QCoreApplication.translate("AppPage", u"Video3", None))
        self.btn_back.setText(QCoreApplication.translate("AppPage", u"\u8fd4\u56de", None))
        self.label_5.setText(QCoreApplication.translate("AppPage", u"X", None))
        self.label_9.setText(QCoreApplication.translate("AppPage", u"\u673a\u5668\u4eba\u8c03\u8bd5\u5f00\u5173", None))
        self.label_20.setText(QCoreApplication.translate("AppPage", u"!", None))
        self.pushButton_3.setText(QCoreApplication.translate("AppPage", u"\u6253\u5f00", None))
        self.pushButton_4.setText(QCoreApplication.translate("AppPage", u"\u5173\u95ed", None))
        self.label_10.setText(QCoreApplication.translate("AppPage", u"X", None))
        self.label_11.setText(QCoreApplication.translate("AppPage", u"\u79fb\u52a8\u8def\u5f84\u70b9\u4f4d\u8c03\u8bd5", None))
        self.label_19.setText(QCoreApplication.translate("AppPage", u"!", None))
        self.pushButton_5.setText(QCoreApplication.translate("AppPage", u"\u79fb\u52a8\u81f3\u8be5\u70b9", None))
        self.pushButton_6.setText(QCoreApplication.translate("AppPage", u"\u4fee\u6539\u70b9\u4f4d", None))
        self.pushButton_7.setText(QCoreApplication.translate("AppPage", u"\u4fdd\u5b58\u70b9\u4f4d", None))
        self.pushButton_8.setText(QCoreApplication.translate("AppPage", u"\u6062\u590d\u9ed8\u8ba4", None))
        self.label_12.setText(QCoreApplication.translate("AppPage", u"X", None))
        self.label_13.setText(QCoreApplication.translate("AppPage", u"\u5438\u6cf5\u8c03\u8bd5", None))
        self.label_15.setText(QCoreApplication.translate("AppPage", u"!", None))
        self.pushButton.setText(QCoreApplication.translate("AppPage", u"\u6253\u5f00", None))
        self.pushButton_2.setText(QCoreApplication.translate("AppPage", u"\u5173\u95ed", None))
        self.btn_start_game.setText(QCoreApplication.translate("AppPage", u"\u5f00\u59cb\u5bf9\u5f08", None))
        self.btn_stop_game.setText(QCoreApplication.translate("AppPage", u"\u7ed3\u675f\u5bf9\u5f08", None))
    # retranslateUi

