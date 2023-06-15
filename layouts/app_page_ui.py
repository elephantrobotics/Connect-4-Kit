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
    QGridLayout, QHBoxLayout, QLabel, QPushButton,
    QSizePolicy, QSpacerItem, QVBoxLayout, QWidget)

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
        self.verticalLayout_4 = QVBoxLayout(self.frame_interact_panel)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.layout_title = QHBoxLayout()
        self.layout_title.setObjectName(u"layout_title")
        self.layout_title.setContentsMargins(10, -1, -1, -1)
        self.label = QLabel(self.frame_interact_panel)
        self.label.setObjectName(u"label")
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setMinimumSize(QSize(48, 48))

        self.layout_title.addWidget(self.label)

        self.label_2 = QLabel(self.frame_interact_panel)
        self.label_2.setObjectName(u"label_2")
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        self.label_2.setStyleSheet(u"font-size : 13pt")

        self.layout_title.addWidget(self.label_2, 0, Qt.AlignLeft)

        self.layout_title.setStretch(0, 1)
        self.layout_title.setStretch(1, 8)

        self.verticalLayout_4.addLayout(self.layout_title)

        self.label_separator = QLabel(self.frame_interact_panel)
        self.label_separator.setObjectName(u"label_separator")
        self.label_separator.setEnabled(True)
        sizePolicy1 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Maximum)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.label_separator.sizePolicy().hasHeightForWidth())
        self.label_separator.setSizePolicy(sizePolicy1)

        self.verticalLayout_4.addWidget(self.label_separator)

        self.layout_cam_selection = QHBoxLayout()
        self.layout_cam_selection.setObjectName(u"layout_cam_selection")
        self.layout_cam_selection.setContentsMargins(10, -1, -1, -1)
        self.label_cam_icon = QLabel(self.frame_interact_panel)
        self.label_cam_icon.setObjectName(u"label_cam_icon")
        sizePolicy.setHeightForWidth(self.label_cam_icon.sizePolicy().hasHeightForWidth())
        self.label_cam_icon.setSizePolicy(sizePolicy)
        self.label_cam_icon.setMinimumSize(QSize(32, 32))

        self.layout_cam_selection.addWidget(self.label_cam_icon)

        self.label_camera_selection = QLabel(self.frame_interact_panel)
        self.label_camera_selection.setObjectName(u"label_camera_selection")
        self.label_camera_selection.setStyleSheet(u"font-size : 12pt\n"
"")
        self.label_camera_selection.setScaledContents(False)
        self.label_camera_selection.setWordWrap(False)

        self.layout_cam_selection.addWidget(self.label_camera_selection)

        self.combo_camera_selection = QComboBox(self.frame_interact_panel)
        self.combo_camera_selection.addItem("")
        self.combo_camera_selection.addItem("")
        self.combo_camera_selection.addItem("")
        self.combo_camera_selection.addItem("")
        self.combo_camera_selection.addItem("")
        self.combo_camera_selection.addItem("")
        self.combo_camera_selection.addItem("")
        self.combo_camera_selection.setObjectName(u"combo_camera_selection")

        self.layout_cam_selection.addWidget(self.combo_camera_selection)

        self.layout_cam_selection.setStretch(0, 1)
        self.layout_cam_selection.setStretch(1, 5)
        self.layout_cam_selection.setStretch(2, 3)

        self.verticalLayout_4.addLayout(self.layout_cam_selection)

        self.horizontalLayout_12 = QHBoxLayout()
        self.horizontalLayout_12.setObjectName(u"horizontalLayout_12")
        self.label_6 = QLabel(self.frame_interact_panel)
        self.label_6.setObjectName(u"label_6")

        self.horizontalLayout_12.addWidget(self.label_6)

        self.switch_video0_on = QCheckBox(self.frame_interact_panel)
        self.switch_video0_on.setObjectName(u"switch_video0_on")

        self.horizontalLayout_12.addWidget(self.switch_video0_on)

        self.horizontalLayout_12.setStretch(0, 9)
        self.horizontalLayout_12.setStretch(1, 1)

        self.verticalLayout_4.addLayout(self.horizontalLayout_12)

        self.horizontalLayout_14 = QHBoxLayout()
        self.horizontalLayout_14.setObjectName(u"horizontalLayout_14")
        self.label_7 = QLabel(self.frame_interact_panel)
        self.label_7.setObjectName(u"label_7")

        self.horizontalLayout_14.addWidget(self.label_7)

        self.switch_video1_on = QCheckBox(self.frame_interact_panel)
        self.switch_video1_on.setObjectName(u"switch_video1_on")
        sizePolicy2 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.switch_video1_on.sizePolicy().hasHeightForWidth())
        self.switch_video1_on.setSizePolicy(sizePolicy2)

        self.horizontalLayout_14.addWidget(self.switch_video1_on)

        self.horizontalLayout_14.setStretch(0, 9)
        self.horizontalLayout_14.setStretch(1, 1)

        self.verticalLayout_4.addLayout(self.horizontalLayout_14)

        self.horizontalLayout_15 = QHBoxLayout()
        self.horizontalLayout_15.setObjectName(u"horizontalLayout_15")
        self.btn_start_camera = QPushButton(self.frame_interact_panel)
        self.btn_start_camera.setObjectName(u"btn_start_camera")

        self.horizontalLayout_15.addWidget(self.btn_start_camera)

        self.btn_stop_camera = QPushButton(self.frame_interact_panel)
        self.btn_stop_camera.setObjectName(u"btn_stop_camera")

        self.horizontalLayout_15.addWidget(self.btn_stop_camera)


        self.verticalLayout_4.addLayout(self.horizontalLayout_15)

        self.layout_algorithm = QVBoxLayout()
        self.layout_algorithm.setObjectName(u"layout_algorithm")
        self.layout_algorithm_title = QHBoxLayout()
        self.layout_algorithm_title.setObjectName(u"layout_algorithm_title")
        self.layout_algorithm_title.setContentsMargins(10, -1, -1, -1)
        self.label_16 = QLabel(self.frame_interact_panel)
        self.label_16.setObjectName(u"label_16")

        self.layout_algorithm_title.addWidget(self.label_16)

        self.label_17 = QLabel(self.frame_interact_panel)
        self.label_17.setObjectName(u"label_17")
        self.label_17.setStyleSheet(u"font-size : 12pt")

        self.layout_algorithm_title.addWidget(self.label_17)

        self.layout_algorithm_title.setStretch(0, 1)
        self.layout_algorithm_title.setStretch(1, 8)

        self.layout_algorithm.addLayout(self.layout_algorithm_title)

        self.frame_algorithm = QFrame(self.frame_interact_panel)
        self.frame_algorithm.setObjectName(u"frame_algorithm")
        self.frame_algorithm.setStyleSheet(u"background : rgb(242, 243, 245)")
        self.frame_algorithm.setFrameShape(QFrame.StyledPanel)
        self.frame_algorithm.setFrameShadow(QFrame.Raised)
        self.verticalLayout_5 = QVBoxLayout(self.frame_algorithm)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.frame_7 = QFrame(self.frame_algorithm)
        self.frame_7.setObjectName(u"frame_7")
        self.frame_7.setStyleSheet(u"background : rgb(236, 240, 241)")
        self.frame_7.setFrameShape(QFrame.StyledPanel)
        self.frame_7.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_2 = QHBoxLayout(self.frame_7)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label_18 = QLabel(self.frame_7)
        self.label_18.setObjectName(u"label_18")

        self.horizontalLayout_2.addWidget(self.label_18)

        self.combo_algs = QComboBox(self.frame_7)
        self.combo_algs.setObjectName(u"combo_algs")

        self.horizontalLayout_2.addWidget(self.combo_algs)

        self.horizontalLayout_2.setStretch(0, 1)
        self.horizontalLayout_2.setStretch(1, 1)

        self.verticalLayout_5.addWidget(self.frame_7)

        self.horizontalLayout_16 = QHBoxLayout()
        self.horizontalLayout_16.setObjectName(u"horizontalLayout_16")
        self.label_8 = QLabel(self.frame_algorithm)
        self.label_8.setObjectName(u"label_8")

        self.horizontalLayout_16.addWidget(self.label_8)

        self.switch_video2_on = QCheckBox(self.frame_algorithm)
        self.switch_video2_on.setObjectName(u"switch_video2_on")

        self.horizontalLayout_16.addWidget(self.switch_video2_on)

        self.horizontalLayout_16.setStretch(0, 9)
        self.horizontalLayout_16.setStretch(1, 1)

        self.verticalLayout_5.addLayout(self.horizontalLayout_16)

        self.horizontalLayout_17 = QHBoxLayout()
        self.horizontalLayout_17.setObjectName(u"horizontalLayout_17")
        self.label_14 = QLabel(self.frame_algorithm)
        self.label_14.setObjectName(u"label_14")

        self.horizontalLayout_17.addWidget(self.label_14)

        self.switch_video3_on = QCheckBox(self.frame_algorithm)
        self.switch_video3_on.setObjectName(u"switch_video3_on")

        self.horizontalLayout_17.addWidget(self.switch_video3_on)

        self.horizontalLayout_17.setStretch(0, 9)
        self.horizontalLayout_17.setStretch(1, 1)

        self.verticalLayout_5.addLayout(self.horizontalLayout_17)

        self.verticalSpacer_3 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_5.addItem(self.verticalSpacer_3)


        self.layout_algorithm.addWidget(self.frame_algorithm)

        self.layout_algorithm.setStretch(0, 1)
        self.layout_algorithm.setStretch(1, 9)

        self.verticalLayout_4.addLayout(self.layout_algorithm)


        self.horizontalLayout_13.addWidget(self.frame_interact_panel)

        self.frame = QFrame(AppPage)
        self.frame.setObjectName(u"frame")
        self.frame.setEnabled(True)
        sizePolicy3 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.frame.sizePolicy().hasHeightForWidth())
        self.frame.setSizePolicy(sizePolicy3)
        self.frame.setStyleSheet(u"background : rgb(242, 243, 245)")
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.verticalLayout_10 = QVBoxLayout(self.frame)
        self.verticalLayout_10.setSpacing(0)
        self.verticalLayout_10.setObjectName(u"verticalLayout_10")
        self.verticalLayout_10.setContentsMargins(10, 40, 10, 10)
        self.frame_8 = QFrame(self.frame)
        self.frame_8.setObjectName(u"frame_8")
        self.frame_8.setStyleSheet(u"background : rgb(255, 255, 255)")
        self.frame_8.setFrameShape(QFrame.StyledPanel)
        self.frame_8.setFrameShadow(QFrame.Raised)
        self.gridLayout = QGridLayout(self.frame_8)
        self.gridLayout.setObjectName(u"gridLayout")
        self.label_video_feed0 = QLabel(self.frame_8)
        self.label_video_feed0.setObjectName(u"label_video_feed0")
        sizePolicy4 = QSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.label_video_feed0.sizePolicy().hasHeightForWidth())
        self.label_video_feed0.setSizePolicy(sizePolicy4)
        self.label_video_feed0.setMinimumSize(QSize(0, 0))
        self.label_video_feed0.setStyleSheet(u"border:1px solid rgb(0, 255, 0);")
        self.label_video_feed0.setScaledContents(False)
        self.label_video_feed0.setMargin(0)

        self.gridLayout.addWidget(self.label_video_feed0, 0, 0, 1, 1)

        self.label_video_feed1 = QLabel(self.frame_8)
        self.label_video_feed1.setObjectName(u"label_video_feed1")
        sizePolicy4.setHeightForWidth(self.label_video_feed1.sizePolicy().hasHeightForWidth())
        self.label_video_feed1.setSizePolicy(sizePolicy4)
        self.label_video_feed1.setStyleSheet(u"border:1px solid rgb(0, 255, 0);")
        self.label_video_feed1.setScaledContents(False)

        self.gridLayout.addWidget(self.label_video_feed1, 0, 1, 1, 1)

        self.label_video_feed2 = QLabel(self.frame_8)
        self.label_video_feed2.setObjectName(u"label_video_feed2")
        sizePolicy4.setHeightForWidth(self.label_video_feed2.sizePolicy().hasHeightForWidth())
        self.label_video_feed2.setSizePolicy(sizePolicy4)
        self.label_video_feed2.setStyleSheet(u"border:1px solid rgb(0, 255, 0);")
        self.label_video_feed2.setScaledContents(False)

        self.gridLayout.addWidget(self.label_video_feed2, 1, 0, 1, 1)

        self.label_video_feed3 = QLabel(self.frame_8)
        self.label_video_feed3.setObjectName(u"label_video_feed3")
        sizePolicy4.setHeightForWidth(self.label_video_feed3.sizePolicy().hasHeightForWidth())
        self.label_video_feed3.setSizePolicy(sizePolicy4)
        self.label_video_feed3.setStyleSheet(u"border:1px solid rgb(0, 255, 0);")
        self.label_video_feed3.setScaledContents(False)

        self.gridLayout.addWidget(self.label_video_feed3, 1, 1, 1, 1)

        self.gridLayout.setRowStretch(0, 1)
        self.gridLayout.setRowStretch(1, 1)
        self.gridLayout.setColumnStretch(0, 1)
        self.gridLayout.setColumnStretch(1, 1)

        self.verticalLayout_10.addWidget(self.frame_8)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_10.addItem(self.verticalSpacer)

        self.verticalLayout_10.setStretch(0, 9)
        self.verticalLayout_10.setStretch(1, 1)

        self.horizontalLayout_13.addWidget(self.frame)

        self.frame_arm_control = QFrame(AppPage)
        self.frame_arm_control.setObjectName(u"frame_arm_control")
        self.frame_arm_control.setStyleSheet(u"background : rgb(242, 243, 245)")
        self.frame_arm_control.setFrameShape(QFrame.StyledPanel)
        self.frame_arm_control.setFrameShadow(QFrame.Raised)
        self.verticalLayout = QVBoxLayout(self.frame_arm_control)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(10, 0, 10, 10)
        self.horizontalLayout_18 = QHBoxLayout()
        self.horizontalLayout_18.setObjectName(u"horizontalLayout_18")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_18.addItem(self.horizontalSpacer)

        self.btn_back = QPushButton(self.frame_arm_control)
        self.btn_back.setObjectName(u"btn_back")
        sizePolicy5 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(self.btn_back.sizePolicy().hasHeightForWidth())
        self.btn_back.setSizePolicy(sizePolicy5)
        self.btn_back.setMinimumSize(QSize(32, 32))

        self.horizontalLayout_18.addWidget(self.btn_back)


        self.verticalLayout.addLayout(self.horizontalLayout_18)

        self.frame_10 = QFrame(self.frame_arm_control)
        self.frame_10.setObjectName(u"frame_10")
        self.frame_10.setStyleSheet(u"")
        self.frame_10.setFrameShape(QFrame.StyledPanel)
        self.frame_10.setFrameShadow(QFrame.Raised)
        self.verticalLayout_9 = QVBoxLayout(self.frame_10)
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.verticalLayout_6 = QVBoxLayout()
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.label_5 = QLabel(self.frame_10)
        self.label_5.setObjectName(u"label_5")

        self.horizontalLayout_5.addWidget(self.label_5)

        self.label_9 = QLabel(self.frame_10)
        self.label_9.setObjectName(u"label_9")

        self.horizontalLayout_5.addWidget(self.label_9)

        self.label_20 = QLabel(self.frame_10)
        self.label_20.setObjectName(u"label_20")

        self.horizontalLayout_5.addWidget(self.label_20)


        self.verticalLayout_6.addLayout(self.horizontalLayout_5)

        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.pushButton_3 = QPushButton(self.frame_10)
        self.pushButton_3.setObjectName(u"pushButton_3")

        self.horizontalLayout_7.addWidget(self.pushButton_3)

        self.pushButton_4 = QPushButton(self.frame_10)
        self.pushButton_4.setObjectName(u"pushButton_4")

        self.horizontalLayout_7.addWidget(self.pushButton_4)


        self.verticalLayout_6.addLayout(self.horizontalLayout_7)


        self.verticalLayout_9.addLayout(self.verticalLayout_6)

        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.label_10 = QLabel(self.frame_10)
        self.label_10.setObjectName(u"label_10")

        self.horizontalLayout_4.addWidget(self.label_10)

        self.label_11 = QLabel(self.frame_10)
        self.label_11.setObjectName(u"label_11")

        self.horizontalLayout_4.addWidget(self.label_11)

        self.label_19 = QLabel(self.frame_10)
        self.label_19.setObjectName(u"label_19")

        self.horizontalLayout_4.addWidget(self.label_19)


        self.verticalLayout_3.addLayout(self.horizontalLayout_4)

        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.pushButton_5 = QPushButton(self.frame_10)
        self.pushButton_5.setObjectName(u"pushButton_5")

        self.horizontalLayout_8.addWidget(self.pushButton_5)

        self.pushButton_6 = QPushButton(self.frame_10)
        self.pushButton_6.setObjectName(u"pushButton_6")

        self.horizontalLayout_8.addWidget(self.pushButton_6)


        self.verticalLayout_3.addLayout(self.horizontalLayout_8)

        self.horizontalLayout_9 = QHBoxLayout()
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.pushButton_7 = QPushButton(self.frame_10)
        self.pushButton_7.setObjectName(u"pushButton_7")

        self.horizontalLayout_9.addWidget(self.pushButton_7)

        self.pushButton_8 = QPushButton(self.frame_10)
        self.pushButton_8.setObjectName(u"pushButton_8")

        self.horizontalLayout_9.addWidget(self.pushButton_8)


        self.verticalLayout_3.addLayout(self.horizontalLayout_9)


        self.verticalLayout_9.addLayout(self.verticalLayout_3)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.label_12 = QLabel(self.frame_10)
        self.label_12.setObjectName(u"label_12")

        self.horizontalLayout_3.addWidget(self.label_12)

        self.label_13 = QLabel(self.frame_10)
        self.label_13.setObjectName(u"label_13")

        self.horizontalLayout_3.addWidget(self.label_13)

        self.label_15 = QLabel(self.frame_10)
        self.label_15.setObjectName(u"label_15")

        self.horizontalLayout_3.addWidget(self.label_15)


        self.verticalLayout_2.addLayout(self.horizontalLayout_3)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.pushButton = QPushButton(self.frame_10)
        self.pushButton.setObjectName(u"pushButton")

        self.horizontalLayout_6.addWidget(self.pushButton)

        self.pushButton_2 = QPushButton(self.frame_10)
        self.pushButton_2.setObjectName(u"pushButton_2")

        self.horizontalLayout_6.addWidget(self.pushButton_2)


        self.verticalLayout_2.addLayout(self.horizontalLayout_6)


        self.verticalLayout_9.addLayout(self.verticalLayout_2)

        self.btn_start_game = QPushButton(self.frame_10)
        self.btn_start_game.setObjectName(u"btn_start_game")

        self.verticalLayout_9.addWidget(self.btn_start_game)

        self.btn_stop_game = QPushButton(self.frame_10)
        self.btn_stop_game.setObjectName(u"btn_stop_game")

        self.verticalLayout_9.addWidget(self.btn_stop_game)


        self.verticalLayout.addWidget(self.frame_10)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer_2)

        self.verticalLayout.setStretch(1, 3)
        self.verticalLayout.setStretch(2, 1)

        self.horizontalLayout_13.addWidget(self.frame_arm_control)

        self.horizontalLayout_13.setStretch(0, 1)
        self.horizontalLayout_13.setStretch(1, 4)
        self.horizontalLayout_13.setStretch(2, 1)

        self.retranslateUi(AppPage)

        self.combo_camera_selection.setCurrentIndex(-1)


        QMetaObject.connectSlotsByName(AppPage)
    # setupUi

    def retranslateUi(self, AppPage):
        AppPage.setWindowTitle(QCoreApplication.translate("AppPage", u"Form", None))
        self.label.setText(QCoreApplication.translate("AppPage", u"ICON", None))
        self.label_2.setText(QCoreApplication.translate("AppPage", u"\u56db\u5b50\u68cb\u5957\u88c5", None))
        self.label_separator.setText(QCoreApplication.translate("AppPage", u"\u5206\u5272\u7ebf", None))
        self.label_cam_icon.setText(QCoreApplication.translate("AppPage", u"ICON", None))
        self.label_camera_selection.setText(QCoreApplication.translate("AppPage", u"\u76f8\u673a\u9009\u62e9", None))
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
        self.label_16.setText(QCoreApplication.translate("AppPage", u"ICON", None))
        self.label_17.setText(QCoreApplication.translate("AppPage", u"\u7b97\u6cd5", None))
        self.label_18.setText(QCoreApplication.translate("AppPage", u"\u6a21\u578b", None))
        self.label_8.setText(QCoreApplication.translate("AppPage", u"\u8bc6\u522b\u6807\u6ce8\u89c6\u9891\u6d41", None))
        self.switch_video2_on.setText("")
        self.label_14.setText(QCoreApplication.translate("AppPage", u"\u7b97\u6cd5\u7ed3\u679c\u5c55\u793a", None))
        self.switch_video3_on.setText("")
        self.label_video_feed0.setText(QCoreApplication.translate("AppPage", u"Video0", None))
        self.label_video_feed1.setText(QCoreApplication.translate("AppPage", u"Video1", None))
        self.label_video_feed2.setText(QCoreApplication.translate("AppPage", u"Video2", None))
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
        self.pushButton_5.setText(QCoreApplication.translate("AppPage", u"\u6253\u5f00", None))
        self.pushButton_6.setText(QCoreApplication.translate("AppPage", u"\u5173\u95ed", None))
        self.pushButton_7.setText(QCoreApplication.translate("AppPage", u"\u6253\u5f00", None))
        self.pushButton_8.setText(QCoreApplication.translate("AppPage", u"\u5173\u95ed", None))
        self.label_12.setText(QCoreApplication.translate("AppPage", u"X", None))
        self.label_13.setText(QCoreApplication.translate("AppPage", u"\u5438\u6cf5\u8c03\u8bd5", None))
        self.label_15.setText(QCoreApplication.translate("AppPage", u"!", None))
        self.pushButton.setText(QCoreApplication.translate("AppPage", u"\u6253\u5f00", None))
        self.pushButton_2.setText(QCoreApplication.translate("AppPage", u"\u5173\u95ed", None))
        self.btn_start_game.setText(QCoreApplication.translate("AppPage", u"\u5f00\u59cb\u5bf9\u5f08", None))
        self.btn_stop_game.setText(QCoreApplication.translate("AppPage", u"\u7ed3\u675f\u5bf9\u5f08", None))
    # retranslateUi

