#!/usr/env/bin python3
# -*- coding: utf-8 -*-
# Author: Aimer Neige
# Mail: aimer.neige@aimerneige.com
# LICENSE: AGPLv3 (https://www.gnu.org/licenses/agpl-3.0.txt)

import re

from PyQt5.QtCore import QSize, pyqtSlot
from PyQt5.QtWidgets import QComboBox, QDesktopWidget, QLabel, QLineEdit, QListWidget, QMainWindow, QMessageBox, QPushButton, QSpinBox
from requests.models import Response

from net.api import Api


window_title = "Student Manage"
window_width = 750
window_height = 330

g_student_list = []


class StudentMainWindow(QMainWindow):
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
        self.initSearchWidgets()
        self.initStudentInfoWidgets()
        self.initCourseWidgets()

    def updateUI(self):
        self.updateStudentData()

    def initSearchWidgets(self):
        self.searchInput = QLineEdit(self)
        self.searchInput.setFixedSize(QSize(100, 30))
        self.searchInput.move(10, 10)

        self.searchButton = QPushButton("Search", self)
        self.searchButton.setFixedSize(QSize(70, 30))
        self.searchButton.move(120, 10)
        self.searchButton.clicked.connect(self.searchButtonClicked)

        self.studentList = QListWidget(self)
        self.studentList.setFixedSize(QSize(180, 230))
        self.studentList.move(10, 50)
        self.studentList.clicked.connect(self.studentListClicked)

        self.resetButton = QPushButton("Reset", self)
        self.resetButton.setFixedSize(QSize(85, 30))
        self.resetButton.move(10, 290)
        self.resetButton.clicked.connect(self.resetButtonClicked)

        self.clearButton = QPushButton("Clear", self)
        self.clearButton.setFixedSize(QSize(85, 30))
        self.clearButton.move(105, 290)
        self.clearButton.clicked.connect(self.clearButtonClicked)

    def initStudentInfoWidgets(self):
        self.idNumberLabel = QLabel("id number:", self)
        self.idNumberLabel.setFixedSize(QSize(80, 30))
        self.idNumberLabel.move(210, 10)

        self.idNumberInput = QLineEdit(self)
        self.idNumberInput.setFixedSize(QSize(190, 30))
        self.idNumberInput.move(300, 10)
        self.idNumberInput.setMaxLength(10)

        self.nameLabel = QLabel("name:", self)
        self.nameLabel.setFixedSize(QSize(80, 30))
        self.nameLabel.move(210, 50)

        self.nameInput = QLineEdit(self)
        self.nameInput.setFixedSize(QSize(190, 30))
        self.nameInput.move(300, 50)

        self.phoneLabel = QLabel("phone:", self)
        self.phoneLabel.setFixedSize(QSize(80, 30))
        self.phoneLabel.move(210, 90)

        self.phoneInput = QLineEdit(self)
        self.phoneInput.setFixedSize(QSize(190, 30))
        self.phoneInput.move(300, 90)
        self.phoneInput.setMaxLength(11)

        self.sexLabel = QLabel("sex:", self)
        self.sexLabel.setFixedSize(QSize(80, 30))
        self.sexLabel.move(210, 130)

        self.sexInput = QComboBox(self)
        self.sexInput.setFixedSize(QSize(190, 30))
        self.sexInput.move(300, 130)
        self.sexInput.addItem("男")
        self.sexInput.addItem("女")

        self.emailLabel = QLabel("mail:", self)
        self.emailLabel.setFixedSize(QSize(80, 30))
        self.emailLabel.move(210, 170)

        self.emailInput = QLineEdit(self)
        self.emailInput.setFixedSize(QSize(190, 30))
        self.emailInput.move(300, 170)

        self.passwordLabel = QLabel("password:", self)
        self.passwordLabel.setFixedSize(QSize(80, 30))
        self.passwordLabel.move(210, 210)

        self.passwordInput = QLineEdit(self)
        self.passwordInput.setFixedSize(QSize(190, 30))
        self.passwordInput.move(300, 210)

        self.ageLabel = QLabel("age:", self)
        self.ageLabel.setFixedSize(QSize(80, 30))
        self.ageLabel.move(210, 250)

        self.ageInput = QSpinBox(self)
        self.ageInput.setFixedSize(QSize(190, 30))
        self.ageInput.move(300, 250)
        self.ageInput.setMinimum(1)

        self.newButton = QPushButton("New", self)
        self.newButton.setFixedSize(QSize(80, 30))
        self.newButton.move(210, 290)
        self.newButton.clicked.connect(self.newButtonClicked)

        self.saveButton = QPushButton("Save", self)
        self.saveButton.setFixedSize(QSize(80, 30))
        self.saveButton.move(310, 290)
        self.saveButton.clicked.connect(self.saveButtonClicked)

        self.deleteButton = QPushButton("Delete", self)
        self.deleteButton.setFixedSize(QSize(80, 30))
        self.deleteButton.move(410, 290)
        self.deleteButton.clicked.connect(self.deleteButtonClicked)

    def initCourseWidgets(self):
        self.courseLabel = QLabel("Courses:", self)
        self.courseLabel.setFixedSize(QSize(80, 20))
        self.courseLabel.move(500, 10)

        self.courseList = QListWidget(self)
        self.courseList.setFixedSize(QSize(240, 240))
        self.courseList.move(500, 40)

        self.courseNewButton = QPushButton("New", self)
        self.courseNewButton.setFixedSize(QSize(70, 30))
        self.courseNewButton.move(500, 290)
        self.courseNewButton.clicked.connect(self.courseNewButtonClicked)

        self.courseDeleteButton = QPushButton("Delete", self)
        self.courseDeleteButton.setFixedSize(QSize(70, 30))
        self.courseDeleteButton.move(580, 290)
        self.courseDeleteButton.clicked.connect(
            self.courseDeleteButtonClicked)

        self.backButton = QPushButton("Back", self)
        self.backButton.setFixedSize(QSize(70, 30))
        self.backButton.move(670, 290)
        self.backButton.clicked.connect(self.backButtonClicked)

    def updateStudentData(self):
        g_student_list.clear()
        self.studentList.clear()
        api = Api()
        response = api.get_all_student()
        if response.json()['message'] != "success":
            QMessageBox.warning(self, "Error", response.json()['data'])
            return
        student_list = response.json()['data']
        for student in student_list:
            g_student_list.append(student)
            self.studentList.insertItem(student['id'], student['name'])

    @pyqtSlot()
    def studentListClicked(self):
        index = self.studentList.currentRow()
        student_id = g_student_list[index]['id']
        api = Api()
        response = api.get_student_by_id(student_id)
        if response.json()['message'] != "success":
            QMessageBox.warning(self, "Error", Response.json()['data'])
            return
        student = response.json()['data']
        self.idNumberInput.setText(student['idNumber'])
        self.nameInput.setText(student['name'])
        self.phoneInput.setText(student['phone'])
        self.sexInput.setCurrentText(student['sex'])
        self.emailInput.setText(student['email'])
        self.passwordInput.setText("")
        self.ageInput.setValue(student['age'])

    @pyqtSlot()
    def searchButtonClicked(self):
        keyword = self.searchInput.text()
        if keyword == "":
            QMessageBox.warning(self, "Error", "Please input search keyword.")
            return
        api = Api()
        response = api.search_student_by_name(keyword)
        if response.json()['message'] != "success":
            QMessageBox.warning(self, "Error", response.json()['data'])
            return
        student_list = response.json()['data']
        g_student_list.clear()
        self.studentList.clear()
        for student in student_list:
            g_student_list.append(student)
            self.studentList.insertItem(student['id'], student['name'])

    @pyqtSlot()
    def resetButtonClicked(self):
        self.searchInput.setText("")
        self.updateStudentData()

    @pyqtSlot()
    def clearButtonClicked(self):
        self.idNumberInput.setText("")
        self.nameInput.setText("")
        self.phoneInput.setText("")
        self.sexInput.setCurrentText("")
        self.emailInput.setText("")
        self.passwordInput.setText("")
        self.ageInput.setValue(1)

    @pyqtSlot()
    def newButtonClicked(self):
        id_number = self.idNumberInput.text()
        name = self.nameInput.text()
        phone = self.phoneInput.text()
        sex = self.sexInput.currentText()
        email = self.emailInput.text()
        password = self.passwordInput.text()
        age = self.ageInput.value()
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
        api = Api()
        response = api.create_new_student(
            id_number, name, phone, sex, email, password, age)
        if response.json()['message'] != 'success':
            QMessageBox.warning(self, "Error", response.json()['data'])
            return
        QMessageBox.information(
            self, "Success", "Create new student successfully.")
        self.updateStudentData()

    @pyqtSlot()
    def saveButtonClicked(self):
        student_index = self.studentList.currentRow()
        student_id = g_student_list[student_index]['id']
        id_number = self.idNumberInput.text()
        name = self.nameInput.text()
        phone = self.phoneInput.text()
        sex = self.sexInput.currentText()
        email = self.emailInput.text()
        password = self.passwordInput.text()
        age = self.ageInput.value()
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
        api = Api()
        response = api.update_student_by_id(
            student_id, id_number, name, phone, sex, email, password, age)
        if response.json()['message'] != 'success':
            QMessageBox.warning(self, "Error", response.json()['data'])
            return
        QMessageBox.information(
            self, "Success", "Save New Student Successfully.")
        self.updateUI()

    @pyqtSlot()
    def deleteButtonClicked(self):
        student_index = self.studentList.currentRow()
        student_id = g_student_list[student_index]['id']
        api = Api()
        response = api.delete_student_by_id(student_id)
        if response.json()['message'] != 'success':
            QMessageBox.warning(self, "Error", response.json()['data'])
            return
        QMessageBox.information(
            self, "Success", "Delete Student Successfully.")
        self.updateUI()

    @pyqtSlot()
    def courseNewButtonClicked(self):
        print("studentNewButtonClicked")

    @pyqtSlot()
    def courseDeleteButtonClicked(self):
        print("studentDeleteButtonClicked")

    @pyqtSlot()
    def backButtonClicked(self) -> None:
        self.close()
        self.father.show()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
