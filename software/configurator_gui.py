# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'configurator_gui.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(846, 615)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QSize(846, 615))
        MainWindow.setMaximumSize(QSize(846, 615))
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.horizontalLayout_4 = QHBoxLayout(self.centralwidget)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(10, 10, 10, 10)
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.refresh_bt = QPushButton(self.centralwidget)
        self.refresh_bt.setObjectName(u"refresh_bt")
        self.refresh_bt.setMinimumSize(QSize(100, 30))

        self.horizontalLayout.addWidget(self.refresh_bt)

        self.coms_cb = QComboBox(self.centralwidget)
        self.coms_cb.setObjectName(u"coms_cb")
        self.coms_cb.setMinimumSize(QSize(120, 30))

        self.horizontalLayout.addWidget(self.coms_cb)

        self.baund_rate_lb = QLabel(self.centralwidget)
        self.baund_rate_lb.setObjectName(u"baund_rate_lb")
        self.baund_rate_lb.setMinimumSize(QSize(0, 30))

        self.horizontalLayout.addWidget(self.baund_rate_lb)

        self.baund_rate_cb = QComboBox(self.centralwidget)
        self.baund_rate_cb.setObjectName(u"baund_rate_cb")
        self.baund_rate_cb.setMinimumSize(QSize(140, 30))

        self.horizontalLayout.addWidget(self.baund_rate_cb)

        self.connection_bt = QPushButton(self.centralwidget)
        self.connection_bt.setObjectName(u"connection_bt")
        self.connection_bt.setMinimumSize(QSize(100, 30))

        self.horizontalLayout.addWidget(self.connection_bt)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.connection_lb = QLabel(self.centralwidget)
        self.connection_lb.setObjectName(u"connection_lb")
        self.connection_lb.setMinimumSize(QSize(150, 30))
        self.connection_lb.setAlignment(Qt.AlignCenter)

        self.horizontalLayout.addWidget(self.connection_lb)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.load_progs_bt = QPushButton(self.centralwidget)
        self.load_progs_bt.setObjectName(u"load_progs_bt")
        self.load_progs_bt.setMinimumSize(QSize(100, 30))

        self.horizontalLayout_2.addWidget(self.load_progs_bt)

        self.progs_cb = QComboBox(self.centralwidget)
        self.progs_cb.setObjectName(u"progs_cb")
        self.progs_cb.setMinimumSize(QSize(120, 30))

        self.horizontalLayout_2.addWidget(self.progs_cb)

        self.rename_bt = QToolButton(self.centralwidget)
        self.rename_bt.setObjectName(u"rename_bt")
        self.rename_bt.setMinimumSize(QSize(0, 30))

        self.horizontalLayout_2.addWidget(self.rename_bt)

        self.add_prog = QToolButton(self.centralwidget)
        self.add_prog.setObjectName(u"add_prog")
        self.add_prog.setMinimumSize(QSize(30, 30))

        self.horizontalLayout_2.addWidget(self.add_prog)

        self.del_prog = QToolButton(self.centralwidget)
        self.del_prog.setObjectName(u"del_prog")
        self.del_prog.setMinimumSize(QSize(30, 30))

        self.horizontalLayout_2.addWidget(self.del_prog)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_2)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.scrollArea = QScrollArea(self.centralwidget)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 802, 403))
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.verticalLayout.addWidget(self.scrollArea)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.update_bt = QPushButton(self.centralwidget)
        self.update_bt.setObjectName(u"update_bt")
        self.update_bt.setMinimumSize(QSize(0, 30))

        self.horizontalLayout_3.addWidget(self.update_bt)

        self.write_bt = QPushButton(self.centralwidget)
        self.write_bt.setObjectName(u"write_bt")
        self.write_bt.setMinimumSize(QSize(0, 30))

        self.horizontalLayout_3.addWidget(self.write_bt)


        self.verticalLayout.addLayout(self.horizontalLayout_3)


        self.horizontalLayout_4.addLayout(self.verticalLayout)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 846, 26))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"The Ant Keypad Configurator", None))
        self.refresh_bt.setText(QCoreApplication.translate("MainWindow", u"Refresh COM", None))
        self.baund_rate_lb.setText(QCoreApplication.translate("MainWindow", u"Baund Rate:", None))
        self.connection_bt.setText(QCoreApplication.translate("MainWindow", u"Connect", None))
        self.connection_lb.setText(QCoreApplication.translate("MainWindow", u"Not Connected", None))
        self.load_progs_bt.setText(QCoreApplication.translate("MainWindow", u"Load Programs", None))
        self.rename_bt.setText(QCoreApplication.translate("MainWindow", u"Rename", None))
        self.add_prog.setText(QCoreApplication.translate("MainWindow", u"+", None))
        self.del_prog.setText(QCoreApplication.translate("MainWindow", u"-", None))
        self.update_bt.setText(QCoreApplication.translate("MainWindow", u"Update Programs", None))
        self.write_bt.setText(QCoreApplication.translate("MainWindow", u"Write Programs on EEPROM", None))
    # retranslateUi

