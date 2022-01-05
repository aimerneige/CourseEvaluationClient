#!/usr/env/bin python3
# -*- coding: utf-8 -*-
# Author: Aimer Neige
# Mail: aimer.neige@aimerneige.com
# LICENSE: AGPLv3 (https://www.gnu.org/licenses/agpl-3.0.txt)


from PyQt5.QtCore import QSize, pyqtSlot
from PyQt5.QtWidgets import QComboBox, QDesktopWidget, QLabel, QListWidget, QMainWindow, QMessageBox, QPlainTextEdit, QPushButton, QLineEdit

from net.api import Api


window_title = "Insert Student"
window_width = 200
window_height = 140


g_student_list = []


class InsertStudentWindow(QMainWindow):
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
        self.label = QLabel("Select a student:", self)
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
        g_student_list.clear()
        self.comboBox.clear()
        api = Api()
        response = api.get_all_student()
        if response.json()['message'] != 'success':
            QMessageBox.warning(self, "Error", response.json()['data'])
            return
        student_list = response.json()['data']
        for student in student_list:
            g_student_list.append(student)
            self.comboBox.insertItem(student['id'], student['name'])
        self.comboBox.setCurrentIndex(-1)

    @pyqtSlot()
    def confirmButtonClicked(self):
        if self.comboBox.currentIndex() == -1:
            QMessageBox.warning(self, "Error", "Please select a student.")
            return
        student_index = self.comboBox.currentIndex()
        student_id = g_student_list[student_index]['id']
        api = Api()
        response = api.add_student_to_course(self.father.courseId, student_id)
        if response.json()['message'] != 'success':
            QMessageBox.warning(self, "Error", response.json()['data'])
            return
        QMessageBox.information(
            self, "Success", "Add student to course successfully.")
        self.close()
        self.father.updateStudentData()

    @pyqtSlot()
    def cancelButtonClicked(self):
        self.close()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
