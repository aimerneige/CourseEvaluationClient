#!/usr/env/bin python3
# -*- coding: utf-8 -*-
# Author: Aimer Neige
# Mail: aimer.neige@aimerneige.com
# LICENSE: AGPLv3 (https://www.gnu.org/licenses/agpl-3.0.txt)


from PyQt5.QtCore import QSize, pyqtSlot
from PyQt5.QtWidgets import QDesktopWidget, QLabel, QMainWindow, QMessageBox, QPushButton, QLineEdit

from net.api import Api


window_title = "Admin Info"
window_width = 300
window_height = 180


class AdminInfoWindow(QMainWindow):
    def __init__(self, father):
        super().__init__()
        self.father = father
        self.initWindow()
        self.initUI()
        self.center()
        self.updateUI()

    def initWindow(self):
        self.setWindowTitle(window_title)
        self.setFixedWidth(window_width)
        self.setFixedHeight(window_height)

    def initUI(self):
        self.initInputWidgets()
        self.initButtons()

    def updateUI(self):
        self.adminId = self.father.adminId
        self.updateAdminData()

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

    def initButtons(self):
        self.backButton = QPushButton("Back", self)
        self.backButton.setFixedSize(QSize(100, 30))
        self.backButton.move(30, 140)
        self.backButton.clicked.connect(self.backButtonClicked)

        self.saveButton = QPushButton("Save", self)
        self.saveButton.setFixedSize(QSize(100, 30))
        self.saveButton.move(170, 140)
        self.saveButton.clicked.connect(self.saveButtonClicked)

    def updateAdminData(self):
        api = Api()
        response = api.get_admin_by_id(self.adminId)
        if response.json()['message'] != 'success':
            QMessageBox.warning(self, "Error", "Error: " +
                                response.json()['data'])
            return
        data = response.json()['data']
        self.nameInput.setText(data['name'])
        self.usernameInput.setText(data['username'])

    @pyqtSlot()
    def backButtonClicked(self):
        self.close()
        self.father.show()

    @pyqtSlot()
    def saveButtonClicked(self):
        name = self.nameInput.text()
        username = self.usernameInput.text()
        password = self.passwordInput.text()
        if name == '' or username == '' or password == '':
            QMessageBox.warning(
                self, "Error", "Please enter name, username and password.")
            return
        api = Api()
        response = api.update_admin_by_id(
            self.adminId, name, username, password)
        if response.json()['message'] == 'success':
            QMessageBox.information(self, "Success", "Update successful.")
        else:
            QMessageBox.warning(self, "Error", "Error: " +
                                response.json()['data'])

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
