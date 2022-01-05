#!/usr/env/bin python3
# -*- coding: utf-8 -*-
# Author: Aimer Neige
# Mail: aimer.neige@aimerneige.com
# LICENSE: AGPLv3 (https://www.gnu.org/licenses/agpl-3.0.txt)


from PyQt5 import QtWidgets
from PyQt5.QtCore import QSize, pyqtSlot
from PyQt5.QtWidgets import QDesktopWidget, QLabel, QLineEdit, QMainWindow, QMessageBox, QPushButton

from net.api import Api
from ui.admin.register import AdminRegisterWindow

window_title = "Admin Login"
window_width = 300
window_height = 140


class AdminLoginWindow(QMainWindow):
    def __init__(self, father) -> None:
        super().__init__()
        self.father = father
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
        self.usernameLabel = QLabel("username:", self)
        self.usernameLabel.setFixedSize(QSize(80, 20))
        self.usernameLabel.move(10, 20)

        self.usernameInput = QLineEdit(self)
        self.usernameInput.setFixedSize(QSize(190, 30))
        self.usernameInput.move(100, 20)

        self.passwordLabel = QLabel("password:", self)
        self.passwordLabel.setFixedSize(QSize(80, 20))
        self.passwordLabel.move(10, 60)

        self.passwordInput = QLineEdit(self)
        self.passwordInput.setFixedSize(QSize(190, 30))
        self.passwordInput.move(100, 60)
        self.passwordInput.setEchoMode(QtWidgets.QLineEdit.Password)

    def initButton(self):
        self.backButton = QPushButton("Back", self)
        self.backButton.setFixedSize(QSize(80, 30))
        self.backButton.move(10, 100)
        self.backButton.clicked.connect(self.backButtonClicked)

        self.loginButton = QPushButton('Login', self)
        self.loginButton.setFixedSize(QSize(80, 30))
        self.loginButton.move(110, 100)
        self.loginButton.clicked.connect(self.loginClicked)

        self.registerButton = QPushButton('Register', self)
        self.registerButton.setFixedSize(QSize(80, 30))
        self.registerButton.move(210, 100)
        self.registerButton.clicked.connect(self.registerClicked)

    @pyqtSlot()
    def backButtonClicked(self) -> None:
        self.close()
        self.father.show()

    @pyqtSlot()
    def loginClicked(self):
        username = self.usernameInput.text()
        password = self.passwordInput.text()
        if username == "" or password == "":
            QMessageBox.warning(
                self, "Warning", "Please enter username and password.")
            return
        api = Api()
        response = api.admin_login(username, password)
        if response.json()['message'] == 'success':
            self.close()
            # todo start manage page
        else:
            QMessageBox.warning(self, 'Error', response.json()['data'])

    @pyqtSlot()
    def registerClicked(self):
        self.close()
        self.adminRegisterWindow = AdminRegisterWindow(self)
        self.adminRegisterWindow.show()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
