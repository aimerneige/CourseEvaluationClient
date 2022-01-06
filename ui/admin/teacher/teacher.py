#!/usr/env/bin python3
# -*- coding: utf-8 -*-
# Author: Aimer Neige
# Mail: aimer.neige@aimerneige.com
# LICENSE: AGPLv3 (https://www.gnu.org/licenses/agpl-3.0.txt)

import re

from PyQt5.QtCore import QSize, pyqtSlot, reset
from PyQt5.QtWidgets import QComboBox, QDesktopWidget, QLabel, QLineEdit, QListWidget, QMainWindow, QMessageBox, QPushButton, QSpinBox
from requests.models import Response

from net.api import Api


window_title = "Teacher Manage"
window_width = 750
window_height = 250

g_teacher_list = []
g_course_list = []


class TeacherMainWindow(QMainWindow):
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
        self.updateTeacherData()

    def initSearchWidgets(self):
        self.searchInput = QLineEdit(self)
        self.searchInput.setFixedSize(QSize(100, 30))
        self.searchInput.move(10, 10)

        self.searchButton = QPushButton("Search", self)
        self.searchButton.setFixedSize(QSize(70, 30))
        self.searchButton.move(120, 10)
        self.searchButton.clicked.connect(self.searchButtonClicked)

        self.teacherList = QListWidget(self)
        self.teacherList.setFixedSize(QSize(180, 150))
        self.teacherList.move(10, 50)
        self.teacherList.clicked.connect(self.teacherListClicked)

        self.resetButton = QPushButton("Reset", self)
        self.resetButton.setFixedSize(QSize(85, 30))
        self.resetButton.move(10, 210)
        self.resetButton.clicked.connect(self.resetButtonClicked)

        self.clearButton = QPushButton("Clear", self)
        self.clearButton.setFixedSize(QSize(85, 30))
        self.clearButton.move(105, 210)
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

        self.ageLabel = QLabel("age:", self)
        self.ageLabel.setFixedSize(QSize(80, 30))
        self.ageLabel.move(210, 170)

        self.ageInput = QSpinBox(self)
        self.ageInput.setFixedSize(QSize(190, 30))
        self.ageInput.move(300, 170)
        self.ageInput.setMinimum(1)

        self.newButton = QPushButton("New", self)
        self.newButton.setFixedSize(QSize(80, 30))
        self.newButton.move(210, 210)
        self.newButton.clicked.connect(self.newButtonClicked)

        self.saveButton = QPushButton("Save", self)
        self.saveButton.setFixedSize(QSize(80, 30))
        self.saveButton.move(310, 210)
        self.saveButton.clicked.connect(self.saveButtonClicked)

        self.deleteButton = QPushButton("Delete", self)
        self.deleteButton.setFixedSize(QSize(80, 30))
        self.deleteButton.move(410, 210)
        self.deleteButton.clicked.connect(self.deleteButtonClicked)

    def initCourseWidgets(self):
        self.courseLabel = QLabel("Courses:", self)
        self.courseLabel.setFixedSize(QSize(80, 30))
        self.courseLabel.move(500, 10)

        self.backButton = QPushButton("Back", self)
        self.backButton.setFixedSize(QSize(70, 30))
        self.backButton.move(670, 10)
        self.backButton.clicked.connect(self.backButtonClicked)

        self.courseList = QListWidget(self)
        self.courseList.setFixedSize(QSize(240, 190))
        self.courseList.move(500, 50)

    def updateTeacherData(self):
        g_teacher_list.clear()
        self.teacherList.clear()
        api = Api()
        response = api.get_all_teacher()
        if response.json()['message'] == 'not found':
            return
        if response.json()['message'] != "success":
            QMessageBox.warning(self, "Error", response.json()['data'])
            return
        teacher_list = response.json()['data']
        for teacher in teacher_list:
            g_teacher_list.append(teacher)
            self.teacherList.insertItem(teacher['id'], teacher['name'])

    def updateCourseData(self, teacher_id):
        g_course_list.clear()
        self.courseList.clear()
        api = Api()
        response = api.get_all_course_by_teacher_id(teacher_id)
        if response.json()['message'] == 'not found':
            return
        if response.json()['message'] != "success":
            QMessageBox.warning(self, "Error", response.json()['data'])
            return
        course_list = response.json()['data']
        for course in course_list:
            g_course_list.append(course)
            self.courseList.insertItem(course['id'], course['title'])

    @pyqtSlot()
    def teacherListClicked(self):
        index = self.teacherList.currentRow()
        teacher_id = g_teacher_list[index]['id']
        api = Api()
        response = api.get_teacher_by_id(teacher_id)
        if response.json()['message'] != "success":
            QMessageBox.warning(self, "Error", Response.json()['data'])
            return
        teacher = response.json()['data']
        self.idNumberInput.setText(teacher['idNumber'])
        self.nameInput.setText(teacher['name'])
        self.phoneInput.setText(teacher['phone'])
        self.sexInput.setCurrentText(teacher['sex'])
        self.ageInput.setValue(teacher['age'])
        self.updateCourseData(teacher_id)

    @pyqtSlot()
    def searchButtonClicked(self):
        keyword = self.searchInput.text()
        if keyword == "":
            QMessageBox.warning(self, "Error", "Please input search keyword.")
            return
        api = Api()
        response = api.search_teacher_by_name(keyword)
        if response.json()['message'] != "success":
            QMessageBox.warning(self, "Error", response.json()['data'])
            return
        teacher_list = response.json()['data']
        g_teacher_list.clear()
        self.teacherList.clear()
        for teacher in teacher_list:
            g_teacher_list.append(teacher)
            self.teacherList.insertItem(teacher['id'], teacher['name'])

    @pyqtSlot()
    def resetButtonClicked(self):
        self.searchInput.setText("")
        self.updateTeacherData()

    @pyqtSlot()
    def clearButtonClicked(self):
        self.idNumberInput.setText("")
        self.nameInput.setText("")
        self.phoneInput.setText("")
        self.sexInput.setCurrentText("")
        self.ageInput.setValue(1)

    @pyqtSlot()
    def newButtonClicked(self):
        id_number = self.idNumberInput.text()
        name = self.nameInput.text()
        phone = self.phoneInput.text()
        sex = self.sexInput.currentText()
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
        if age == 0:
            QMessageBox.warning(self, "Warning", "Please input age.")
            return
        api = Api()
        response = api.create_new_teacher(
            id_number, name, phone, sex, age)
        if response.json()['message'] != 'success':
            QMessageBox.warning(self, "Error", response.json()['data'])
            return
        QMessageBox.information(
            self, "Success", "Create new teacher successfully.")
        self.updateTeacherData()

    @pyqtSlot()
    def saveButtonClicked(self):
        teacher_index = self.teacherList.currentRow()
        teacher_id = g_teacher_list[teacher_index]['id']
        id_number = self.idNumberInput.text()
        name = self.nameInput.text()
        phone = self.phoneInput.text()
        sex = self.sexInput.currentText()
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
        if age == 0:
            QMessageBox.warning(self, "Warning", "Please input age.")
            return
        api = Api()
        response = api.update_teacher_by_id(
            teacher_id, id_number, name, phone, sex, age)
        if response.json()['message'] != 'success':
            QMessageBox.warning(self, "Error", response.json()['data'])
            return
        QMessageBox.information(
            self, "Success", "Save teacher successfully.")
        self.updateUI()

    @pyqtSlot()
    def deleteButtonClicked(self):
        teacher_index = self.teacherList.currentRow()
        teacher_id = g_teacher_list[teacher_index]['id']
        api = Api()
        response = api.delete_teacher_by_id(teacher_id)
        if response.json()['message'] != 'success':
            QMessageBox.warning(self, "Error", response.json()['data'])
            return
        QMessageBox.information(
            self, "Success", "Delete teacher successfully.")
        self.updateUI()

    @pyqtSlot()
    def backButtonClicked(self) -> None:
        self.close()
        self.father.show()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
