#!/usr/env/bin python3
# -*- coding: utf-8 -*-
# Author: Aimer Neige
# Mail: aimer.neige@aimerneige.com
# LICENSE: AGPLv3 (https://www.gnu.org/licenses/agpl-3.0.txt)


from PyQt5.QtCore import QSize, pyqtSlot
from PyQt5.QtWidgets import QDesktopWidget, QMainWindow, QPushButton

from ui.admin.login import AdminLogin


window_title = "Course Evaluation"
window_width = 300
window_height = 140


class Window(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.initWindow()
        self.initUI()
        self.center()

    def initWindow(self) -> None:
        """
        Init window properties.
        """
        self.setWindowTitle(window_title)
        self.setFixedWidth(window_width)
        self.setFixedHeight(window_height)

    def initUI(self) -> None:
        """
        Init UI widgets and layout.
        """
        self.initAdminButton()
        self.initStudentButton()

    def initAdminButton(self) -> None:
        """
        Init admin button.
        """
        self.adminLoginButton = QPushButton("Admin Login", self)
        self.adminLoginButton.setFixedSize(QSize(120, 40))
        self.adminLoginButton.move(80, 20)
        self.adminLoginButton.clicked.connect(self.adminLoginClicked)

    def initStudentButton(self) -> None:
        """
        Init student button.
        """
        self.studentLoginButton = QPushButton("Student Login", self)
        self.studentLoginButton.setFixedSize(QSize(120, 40))
        self.studentLoginButton.move(80, 80)
        self.studentLoginButton.clicked.connect(self.studentLoginClicked)

    def center(self) -> None:
        """
        Center the window on the screen.
        """
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    @pyqtSlot()
    def adminLoginClicked(self) -> None:
        """
        Admin login button clicked.
        """
        print('admin login')
        self.close()
        self.adminLoginPage = AdminLogin()
        self.adminLoginPage.show()

    @pyqtSlot()
    def studentLoginClicked(self) -> None:
        """
        Student login button clicked.
        """
        print('student login')
