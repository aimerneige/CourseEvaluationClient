#!/usr/env/bin python3
# -*- coding: utf-8 -*-
# Author: Aimer Neige
# Mail: aimer.neige@aimerneige.com
# LICENSE: AGPLv3 (https://www.gnu.org/licenses/agpl-3.0.txt)


from PyQt5.QtCore import QSize, pyqtSlot, reset
from PyQt5.QtWidgets import QComboBox, QDesktopWidget, QLabel, QListWidget, QMainWindow, QMessageBox, QPlainTextEdit, QPushButton, QSpinBox
from requests.models import Response
from net import api

from net.api import Api

window_title = "Create Evaluation"
window_width = 200
window_height = 140

g_course_list = []


class CreateEvaluationWindow(QMainWindow):
    def __init__(self, father):
        super().__init__()
        self.father = father
        self.initWindow()
        self.initUI()
        self.updateUI()
        self.center()

    def initWindow(self):
        self.setWindowTitle(window_title)
        self.setFixedWidth(window_width)
        self.setFixedHeight(window_height)

    def initUI(self):
        self.label = QLabel("Select a course:", self)
        self.label.setFixedSize(QSize(180, 20))
        self.label.move(10, 10)

        self.comboBox = QComboBox(self)
        self.comboBox.setFixedSize(QSize(180, 30))
        self.comboBox.move(10, 40)

        self.confirmButton = QPushButton("Confirm", self)
        self.confirmButton.setFixedSize(QSize(80, 30))
        self.confirmButton.move(10, 80)
        self.confirmButton.clicked.connect(self.confirmButtonClicked)

        self.cancelButton = QPushButton("Cancel", self)
        self.cancelButton.setFixedSize(QSize(80, 30))
        self.cancelButton.move(100, 80)
        self.cancelButton.clicked.connect(self.cancelButtonClicked)

    def updateUI(self):
        g_course_list.clear()
        self.comboBox.clear()
        api = Api()
        response = api.get_all_course()
        if response.json()['message'] != 'success':
            QMessageBox.warning(self, "Error", "Failed to get course list")
            return
        course_list = response.json()['data']
        for course in course_list:
            g_course_list.append(course)
            self.comboBox.insertItem(self.comboBox.count(), course['title'])
        self.comboBox.setCurrentIndex(-1)

    @pyqtSlot()
    def confirmButtonClicked(self):
        if self.comboBox.currentIndex() == -1:
            QMessageBox.warning(self, "Error", "Please select a course")
            return
        course_index = self.comboBox.currentIndex()
        course_id = g_course_list[course_index]['id']
        api = Api()
        student_response = api.get_all_students_by_course_id(course_id)
        if student_response.json()['message'] != 'success':
            QMessageBox.warning(self, "Error", student_response.json()['data'])
            return
        student_list = student_response.json()['data']
        for student in student_list:
            student_id = student['id']
            evaluation_response = api.create_new_evaluation(
                student_id, course_id)
            if evaluation_response.json()['message'] != 'success':
                QMessageBox.warning(
                    self, "Error", evaluation_response.json()['data'])
                return
        QMessageBox.information(self, "Success", "Evaluation created")

    @pyqtSlot()
    def cancelButtonClicked(self):
        self.close()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
