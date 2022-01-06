#!/usr/env/bin python3
# -*- coding: utf-8 -*-
# Author: Aimer Neige
# Mail: aimer.neige@aimerneige.com
# LICENSE: AGPLv3 (https://www.gnu.org/licenses/agpl-3.0.txt)

from functools import update_wrapper
from PyQt5.QtCore import QSize, pyqtSlot
from PyQt5.QtWidgets import QDesktopWidget, QLabel, QListWidget, QMainWindow, QMessageBox, QPushButton

from net.api import Api
from ui.student.question import StudentQuestionWindow


window_title = "Student Main"
window_width = 200
window_height = 330

g_evaluation_list = []


class StudentMainWindow(QMainWindow):
    def __init__(self, father):
        super().__init__()
        self.father = father
        self.evaluationId = 0
        self.initWindow()
        self.initUI()
        self.updateUI()
        self.center()

    def initWindow(self):
        self.setWindowTitle(window_title)
        self.setFixedWidth(window_width)
        self.setFixedHeight(window_height)

    def initUI(self):
        self.taskLabel = QLabel("Task:", self)
        self.taskLabel.setFixedSize(QSize(180, 30))
        self.taskLabel.move(10, 10)

        self.evaluationList = QListWidget(self)
        self.evaluationList.setFixedSize(QSize(180, 200))
        self.evaluationList.move(10, 40)
        self.evaluationList.clicked.connect(self.evaluationListClicked)

        self.startButton = QPushButton("Start", self)
        self.startButton.setFixedSize(QSize(180, 30))
        self.startButton.move(10, 250)
        self.startButton.clicked.connect(self.startButtonClicked)

        self.backButton = QPushButton("Back", self)
        self.backButton.setFixedSize(QSize(180, 30))
        self.backButton.move(10, 290)
        self.backButton.clicked.connect(self.backButtonClicked)

    def updateUI(self):
        self.studentId = self.father.studentId
        self.updateEvaluationData()

    def updateEvaluationData(self):
        g_evaluation_list.clear()
        self.evaluationList.clear()
        api = Api()
        response = api.get_all_evaluation_by_student_id(self.studentId)
        if response.json()['message'] == 'not found':
            return
        if response.json()['message'] != 'success':
            QMessageBox.warning(self, "Error", response.json()['data'])
            return
        evaluation_list = response.json()['data']
        for evaluation in evaluation_list:
            if len(evaluation['questionIds']) != 0:
                continue
            course_id = evaluation['courseId']
            course_response = api.get_course_by_id(course_id)
            if course_response.json()['message'] != 'success':
                QMessageBox.warning(
                    self, "Error", course_response.json()['data'])
                return
            course = course_response.json()['data']
            g_evaluation_list.append(evaluation)
            self.evaluationList.insertItem(evaluation['id'], course['title'])

    @pyqtSlot()
    def evaluationListClicked(self):
        index = self.evaluationList.currentRow()
        evaluation_id = g_evaluation_list[index]['id']
        self.evaluationId = evaluation_id

    @pyqtSlot()
    def startButtonClicked(self):
        self.close()
        self.studentEvaluationWindow = StudentQuestionWindow(self)
        self.studentEvaluationWindow.show()

    @pyqtSlot()
    def backButtonClicked(self) -> None:
        self.close()
        self.father.show()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
