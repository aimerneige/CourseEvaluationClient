#!/usr/env/bin python3
# -*- coding: utf-8 -*-
# Author: Aimer Neige
# Mail: aimer.neige@aimerneige.com
# LICENSE: AGPLv3 (https://www.gnu.org/licenses/agpl-3.0.txt)


from PyQt5 import QtWidgets
from PyQt5.QtCore import QSize, pyqtSlot
from PyQt5.QtWidgets import QDesktopWidget, QLabel, QLineEdit, QMainWindow, QMessageBox, QPushButton

from net.api import Api

window_title = "Admin Register"
window_width = 300
window_height = 180


class AdminRegisterWindow(QMainWindow):
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
        self.initLoginWarning()

    def initInputWidgets(self):
        self.nameLabel = QLabel("name:", self)
        self.nameLabel.setFixedSize(QSize(80, 20))
        self.nameLabel.move(10, 20)

        self.nameInput = QLineEdit(self)
        self.nameInput.setFixedSize(QSize(190, 30))
        self.nameInput.move(100, 20)

        self.usernameLabel = QLabel("username:", self)
        self.usernameLabel.setFixedSize(QSize(80, 20))
        self.usernameLabel.move(10, 60)

        self.usernameInput = QLineEdit(self)
        self.usernameInput.setFixedSize(QSize(190, 30))
        self.usernameInput.move(100, 60)

        self.passwordLabel = QLabel("password:", self)
        self.passwordLabel.setFixedSize(QSize(80, 20))
        self.passwordLabel.move(10, 100)

        self.passwordInput = QLineEdit(self)
        self.passwordInput.setFixedSize(QSize(190, 30))
        self.passwordInput.move(100, 100)
        self.passwordInput.setEchoMode(QtWidgets.QLineEdit.Password)

    def initButton(self):
        self.backButton = QPushButton('Back', self)
        self.backButton.setFixedSize(QSize(80, 30))
        self.backButton.move(10, 140)
        self.backButton.clicked.connect(self.backButtonClicked)

        self.loginButton = QPushButton('Login', self)
        self.loginButton.setFixedSize(QSize(80, 30))
        self.loginButton.move(110, 140)
        self.loginButton.clicked.connect(self.loginClicked)

        self.registerButton = QPushButton('Register', self)
        self.registerButton.setFixedSize(QSize(80, 30))
        self.registerButton.move(210, 140)
        self.registerButton.clicked.connect(self.registerClicked)

    def initLoginWarning(self):
        self.nameLabel.setVisible(False)
        self.nameInput.setVisible(False)
        self.registerButton.setDisabled(True)
        self.loginButton.setDisabled(False)

        self.warningLabel = QLabel(
            "You must login a admin account first!", self)
        self.warningLabel.setFixedSize(QSize(280, 20))
        self.warningLabel.move(10, 20)

    def closeLoginWarning(self):
        self.nameLabel.setVisible(True)
        self.nameInput.setVisible(True)

        self.usernameInput.setText("")
        self.passwordInput.setText("")
        self.passwordInput.setEchoMode(QtWidgets.QLineEdit.Normal)

        self.warningLabel.setVisible(False)
        self.registerButton.setDisabled(False)
        self.loginButton.setDisabled(True)

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
            self.closeLoginWarning()
        else:
            QMessageBox.warning(self, 'Error', response.json()['data'])

    @pyqtSlot()
    def registerClicked(self):
        name = self.nameInput.text()
        username = self.usernameInput.text()
        password = self.passwordInput.text()
        if name == "" or username == "" or password == "":
            QMessageBox.warning(
                self, "Warning", "Please enter name, username and password.")
            return
        api = Api()
        response = api.create_new_admin(name, username, password)
        if response.json()['message'] == 'success':
            QMessageBox.information(self, 'Success', "Register successful.")
        else:
            QMessageBox.warning(self, 'Error', response.json()['data'])

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
