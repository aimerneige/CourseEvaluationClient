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
        self.studentId = 0
        self.initWindow()
        self.initUI()
        self.center()

    def initWindow(self):
        self.setWindowTitle(window_title)
        self.setFixedWidth(window_width)
        self.setFixedHeight(window_height)

    def initUI(self):
        self.initInputWidgets()
        self.initButton()

    def initInputWidgets(self):
        self.idNumberLabel = QLabel("id number:", self)
        self.idNumberLabel.setFixedSize(QSize(80, 20))
        self.idNumberLabel.move(10, 20)

        self.idNumberInput = QLineEdit(self)
        self.idNumberInput.setFixedSize(QSize(190, 30))
        self.idNumberInput.move(100, 20)

        self.passwordLabel = QLabel("password:", self)
        self.passwordLabel.setFixedSize(QSize(80, 20))
        self.passwordLabel.move(10, 60)

        self.passwordInput = QLineEdit(self)
        self.passwordInput.setFixedSize(QSize(190, 30))
        self.passwordInput.move(100, 60)
        self.passwordInput.setEchoMode(QtWidgets.QLineEdit.Password)

    def initButton(self):
        self.backButton = QPushButton("Back", self)
        self.backButton.setFixedSize(button_size)
        self.backButton.move(10, 100)
        self.backButton.clicked.connect(self.backButtonClicked)

        self.loginButton = QPushButton('Login', self)
        self.loginButton.setFixedSize(button_size)
        self.loginButton.move(110, 100)
        self.loginButton.clicked.connect(self.loginClicked)

        self.registerButton = QPushButton('Register', self)
        self.registerButton.setFixedSize(button_size)
        self.registerButton.move(210, 100)
        self.registerButton.clicked.connect(self.registerClicked)

    @pyqtSlot()
    def backButtonClicked(self) -> None:
        self.close()
        self.father.show()

    @pyqtSlot()
    def loginClicked(self):
        id_number = self.idNumberInput.text()
        password = self.passwordInput.text()
        if id_number == "" or password == "":
            QMessageBox.warning(
                self, "Warning", "Please input id number and password.")
            return
        api = Api()
        response = api.student_login(id_number, password)
        if response.json()['message'] == 'success':
            self.studentId = response.json()['data']['id']
            self.close()
            # start student main window
        else:
            QMessageBox.warning(self, 'Error', response.json()['data'])

    @pyqtSlot()
    def registerClicked(self):
        self.close()
        # todo start register window

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
