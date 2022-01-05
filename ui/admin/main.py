#!/usr/env/bin python3
# -*- coding: utf-8 -*-
# Author: Aimer Neige
# Mail: aimer.neige@aimerneige.com
# LICENSE: AGPLv3 (https://www.gnu.org/licenses/agpl-3.0.txt)


from PyQt5.QtCore import QSize, pyqtSlot
from PyQt5.QtWidgets import QDesktopWidget, QGridLayout, QMainWindow, QPushButton, QWidget
from ui.admin.course.course import CourseMainWindow
from ui.admin.evaluation.evaluation import EvaluationMainWindow

from ui.admin.info.info import AdminInfoWindow
from ui.admin.student.student import StudentMainWindow
from ui.admin.teacher.teacher import TeacherMainWindow


window_title = "Admin Manage"
window_width = 300
window_height = 130

button_size = QSize(100, 30)


class AdminMainWindow(QMainWindow):
    def __init__(self, father):
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
        self.courseButton = QPushButton("Course", self)
        self.courseButton.setFixedSize(button_size)
        self.courseButton.move(40, 10)
        self.courseButton.clicked.connect(self.courseButtonClicked)

        self.evaluationButton = QPushButton("Evaluation", self)
        self.evaluationButton.setFixedSize(button_size)
        self.evaluationButton.move(170, 10)
        self.evaluationButton.clicked.connect(self.evaluationButtonClicked)

        self.teacherButton = QPushButton("Teacher", self)
        self.teacherButton.setFixedSize(button_size)
        self.teacherButton.move(40, 50)
        self.teacherButton.clicked.connect(self.teacherButtonClicked)

        self.studentButton = QPushButton("Student", self)
        self.studentButton.setFixedSize(button_size)
        self.studentButton.move(170, 50)
        self.studentButton.clicked.connect(self.studentButtonClicked)

        self.infoButton = QPushButton("Info", self)
        self.infoButton.setFixedSize(button_size)
        self.infoButton.move(40, 90)
        self.infoButton.clicked.connect(self.infoButtonClicked)

        self.backButton = QPushButton("Back", self)
        self.backButton.setFixedSize(button_size)
        self.backButton.move(170, 90)
        self.backButton.clicked.connect(self.backButtonClicked)

    @pyqtSlot()
    def courseButtonClicked(self):
        self.close()
        self.courseMainWindow = CourseMainWindow(self)
        self.courseMainWindow.show()

    @pyqtSlot()
    def evaluationButtonClicked(self):
        self.close()
        self.evaluationMainWindow = EvaluationMainWindow(self)
        self.evaluationMainWindow.show()

    @pyqtSlot()
    def teacherButtonClicked(self):
        self.close()
        self.teacherMainWindow = TeacherMainWindow(self)
        self.teacherMainWindow.show()

    @pyqtSlot()
    def studentButtonClicked(self):
        self.close()
        self.studentMainWindow = StudentMainWindow(self)
        self.studentMainWindow.show()

    @pyqtSlot()
    def infoButtonClicked(self):
        self.close()
        self.adminInfoWindow = AdminInfoWindow(self)
        self.adminInfoWindow.show()

    @pyqtSlot()
    def backButtonClicked(self):
        self.close()
        self.father.show()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
