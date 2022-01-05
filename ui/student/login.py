#!/usr/env/bin python3
# -*- coding: utf-8 -*-
# Author: Aimer Neige
# Mail: aimer.neige@aimerneige.com
# LICENSE: AGPLv3 (https://www.gnu.org/licenses/agpl-3.0.txt)


from PyQt5 import QtWidgets
from PyQt5.QtCore import QSize, pyqtSlot
from PyQt5.QtWidgets import QDesktopWidget, QLabel, QLineEdit, QMainWindow, QMessageBox, QPushButton

from net.api import Api
from ui.admin.main import AdminMainWindow
from ui.admin.register import AdminRegisterWindow


window_title = "Student Login"
window_width = 300
window_height = 140

button_size = QSize(80, 30)


class StudentLoginWindow(QMainWindow):
    def __init__(self, father):
        super().__init__()
        self.father = father
        self.adminId = 0
        self.initWindow()
        self.initUI()
        self.center()

    def initWindow(self):
        self.setWindowTitle(window_title)
        self.setFixedWidth(window_width)
        self.setFixedHeight(window_height)

    def initUI(self):
        pass

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
