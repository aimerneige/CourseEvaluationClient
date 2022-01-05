#!/usr/env/bin python3
# -*- coding: utf-8 -*-
# Author: Aimer Neige
# Mail: aimer.neige@aimerneige.com
# LICENSE: AGPLv3 (https://www.gnu.org/licenses/agpl-3.0.txt)


from PyQt5 import QtWidgets
from PyQt5.QtCore import QSize, pyqtSlot
from PyQt5.QtWidgets import QDesktopWidget, QLabel, QLineEdit, QMessageBox, QPushButton, QWidget

from net.web_requsets import WebRequests


class AdminLogin(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.setFixedSize(300, 140)
        self.initUI()
        self.center()

    def initUI(self) -> None:
        self.initInput()
        self.initButton()

    def initInput(self) -> None:
        """
        Init input widgets.
        """
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

    def initButton(self) -> None:
        """
        Init button widgets.
        """
        self.loginButton = QPushButton('Login', self)
        self.loginButton.setFixedSize(QSize(100, 30))
        self.loginButton.move(20, 100)
        self.loginButton.clicked.connect(self.loginClicked)

        self.registerButton = QPushButton('Register', self)
        self.registerButton.setFixedSize(QSize(100, 30))
        self.registerButton.move(180, 100)
        self.registerButton.clicked.connect(self.registerClicked)


    @pyqtSlot()
    def loginClicked(self) -> None:
        """
        Login.
        """
        username = self.usernameInput.text()
        password = self.passwordInput.text()
        web_requsets = WebRequests()
        response = web_requsets.admin_login(username, password)
        if response.json()['message'] == 'success':
            self.close()
            # todo start manage page
        else:
            QMessageBox.warning(self, 'Error', response.json()['data'])

    @pyqtSlot()
    def registerClicked(self) -> None:
        """
        Register.
        """
        pass

    def center(self) -> None:
        """
        Center the window on the screen.
        """
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
