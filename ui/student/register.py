#!/usr/env/bin python3
# -*- coding: utf-8 -*-
# Author: Aimer Neige
# Mail: aimer.neige@aimerneige.com
# LICENSE: AGPLv3 (https://www.gnu.org/licenses/agpl-3.0.txt)

import re

from PyQt5 import QtWidgets
from PyQt5.QtCore import QSize, pyqtSlot
from PyQt5.QtWidgets import QComboBox, QDesktopWidget, QLabel, QLineEdit, QMainWindow, QMessageBox, QPushButton, QSpinBox

from net.api import Api

window_title = "Student Register"
window_width = 300
window_height = 370


class StudentRegisterWindow(QMainWindow):
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
        self.idNumberLabel = QLabel("id number:", self)
        self.idNumberLabel.setFixedSize(QSize(80, 20))
        self.idNumberLabel.move(10, 10)

        self.idNumberInput = QLineEdit(self)
        self.idNumberInput.setFixedSize(QSize(190, 30))
        self.idNumberInput.move(100, 10)
        self.idNumberInput.setMaxLength(10)

        self.nameLabel = QLabel("name:", self)
        self.nameLabel.setFixedSize(QSize(80, 20))
        self.nameLabel.move(10, 50)

        self.nameInput = QLineEdit(self)
        self.nameInput.setFixedSize(QSize(190, 30))
        self.nameInput.move(100, 50)

        self.phoneLabel = QLabel("phone:", self)
        self.phoneLabel.setFixedSize(QSize(80, 20))
        self.phoneLabel.move(10, 90)

        self.phoneInput = QLineEdit(self)
        self.phoneInput.setFixedSize(QSize(190, 30))
        self.phoneInput.move(100, 90)
        self.phoneInput.setMaxLength(11)

        self.sexLabel = QLabel("sex:", self)
        self.sexLabel.setFixedSize(QSize(80, 20))
        self.sexLabel.move(10, 130)

        self.sexInput = QComboBox(self)
        self.sexInput.setFixedSize(QSize(190, 30))
        self.sexInput.move(100, 130)
        self.sexInput.addItem("男")
        self.sexInput.addItem("女")

        self.emailLabel = QLabel("mail:", self)
        self.emailLabel.setFixedSize(QSize(80, 20))
        self.emailLabel.move(10, 170)

        self.emailInput = QLineEdit(self)
        self.emailInput.setFixedSize(QSize(190, 30))
        self.emailInput.move(100, 170)

        self.passwordLabel = QLabel("password:", self)
        self.passwordLabel.setFixedSize(QSize(80, 20))
        self.passwordLabel.move(10, 210)

        self.passwordInput = QLineEdit(self)
        self.passwordInput.setFixedSize(QSize(190, 30))
        self.passwordInput.move(100, 210)

        self.ageLabel = QLabel("age:", self)
        self.ageLabel.setFixedSize(QSize(80, 20))
        self.ageLabel.move(10, 250)

        self.ageInput = QSpinBox(self)
        self.ageInput.setFixedSize(QSize(190, 30))
        self.ageInput.move(100, 250)
        self.ageInput.setMinimum(1)

        self.verifyCodeLabel = QLabel("verify code:", self)
        self.verifyCodeLabel.setFixedSize(QSize(80, 20))
        self.verifyCodeLabel.move(10, 290)

        self.verifyCodeInput = QLineEdit(self)
        self.verifyCodeInput.setFixedSize(QSize(100, 30))
        self.verifyCodeInput.move(100, 290)

    def initButton(self):
        self.backButton = QPushButton('Back', self)
        self.backButton.setFixedSize(QSize(120, 30))
        self.backButton.move(10, 330)
        self.backButton.clicked.connect(self.backButtonClicked)

        self.sendMailButton = QPushButton('Send Mail', self)
        self.sendMailButton.setFixedSize(QSize(80, 30))
        self.sendMailButton.move(210, 290)
        self.sendMailButton.clicked.connect(self.sendMailClicked)

        self.registerButton = QPushButton('Register', self)
        self.registerButton.setFixedSize(QSize(120, 30))
        self.registerButton.move(170, 330)
        self.registerButton.clicked.connect(self.registerClicked)

    @pyqtSlot()
    def backButtonClicked(self) -> None:
        self.close()
        self.father.show()

    @pyqtSlot()
    def sendMailClicked(self):
        email = self.emailInput.text()
        if email == "":
            QMessageBox.warning(self, "Warning", "Please input mail.")
            return
        if not re.match(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', email):
            QMessageBox.warning(self, "Warning", "Please input correct mail.")
            return
        api = Api()
        response = api.send_verify_mail(email)
        if response.json()["message"] == "success":
            QMessageBox.information(
                self, "Information", "Verify code has been sent to your mail.")
        else:
            QMessageBox.warning(
                self, "Warning", "Send verify code failed.\n" + response["data"])

    @pyqtSlot()
    def registerClicked(self):
        id_number = self.idNumberInput.text()
        name = self.nameInput.text()
        phone = self.phoneInput.text()
        sex = self.sexInput.currentText()
        email = self.emailInput.text()
        password = self.passwordInput.text()
        age = self.ageInput.value()
        verify_code = self.verifyCodeInput.text()
        if id_number == "":
            QMessageBox.warning(self, "Warning", "Please input id number.")
            return
        if name == "":
            QMessageBox.warning(self, "Warning", "Please input name.")
            return
        if phone == "":
            QMessageBox.warning(self, "Warning", "Please input phone.")
            return
        if sex != "男" and sex != "女":
            QMessageBox.warning(self, "Warning", "Please select sex.")
            return
        if email == "":
            QMessageBox.warning(self, "Warning", "Please input mail.")
            return
        if not re.match(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', email):
            QMessageBox.warning(self, "Warning", "Please input correct mail.")
            return
        if password == "":
            QMessageBox.warning(self, "Warning", "Please input password.")
            return
        if age == 0:
            QMessageBox.warning(self, "Warning", "Please input age.")
            return
        if verify_code == "":
            QMessageBox.warning(self, "Warning", "Please input verify code.")
            return
        api = Api()
        response = api.register_new_student(
            id_number, name, phone, sex, email, password, age, verify_code)
        if response.json()['message'] == 'success':
            QMessageBox.information(self, "Success", "Register successful.")
        else:
            QMessageBox.warning(self, "Error", "Error: " +
                                response.json()['data'])

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
