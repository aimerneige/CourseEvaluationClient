#!/usr/env/bin python3
# -*- coding: utf-8 -*-
# Author: Aimer Neige
# Mail: aimer.neige@aimerneige.com
# LICENSE: AGPLv3 (https://www.gnu.org/licenses/agpl-3.0.txt)


from PyQt5.QtCore import QSize, pyqtSlot, reset
from PyQt5.QtWidgets import QDesktopWidget, QLabel, QListWidget, QMainWindow, QMessageBox, QPlainTextEdit, QPushButton, QSpinBox

from net.api import Api
from ui.admin import evaluation
from ui.admin.evaluation.create import CreateEvaluationWindow


window_title = "Evaluation Manage"
window_width = 600
window_height = 330

g_evaluation_list = []
g_question_list = []


class EvaluationMainWindow(QMainWindow):
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
        self.initEvaluationWidgets()
        self.initQuestionWidgets()
        self.initAnswerWidgets()
        self.initBackButton()

    def updateUI(self):
        self.updateEvaluationList()

    def initEvaluationWidgets(self):
        self.evaluationLabel = QLabel("Evaluation:", self)
        self.evaluationLabel.setFixedSize(QSize(80, 30))
        self.evaluationLabel.move(10, 10)

        self.evaluationNewButton = QPushButton("New", self)
        self.evaluationNewButton.setFixedSize(QSize(80, 30))
        self.evaluationNewButton.move(110, 10)
        self.evaluationNewButton.clicked.connect(self.courseNewButtonClicked)

        self.evaluationList = QListWidget(self)
        self.evaluationList.setFixedSize(QSize(180, 270))
        self.evaluationList.move(10, 50)
        self.evaluationList.clicked.connect(self.evaluationListClicked)

    def initQuestionWidgets(self):
        self.questionLabel = QLabel("Question:", self)
        self.questionLabel.setFixedSize(QSize(80, 30))
        self.questionLabel.move(200, 10)

        self.questionList = QListWidget(self)
        self.questionList.setFixedSize(QSize(220, 270))
        self.questionList.move(200, 50)
        self.questionList.clicked.connect(self.questionListClicked)

    def initAnswerWidgets(self):
        self.markLabel = QLabel("Mark:", self)
        self.markLabel.setFixedSize(QSize(80, 30))
        self.markLabel.move(430, 10)

        self.markValue = QSpinBox(self)
        self.markValue.setReadOnly(True)
        self.markValue.setFixedSize(QSize(80, 30))
        self.markValue.move(510, 10)

        self.praiseLabel = QLabel("Praise:", self)
        self.praiseLabel.setFixedSize(QSize(80, 30))
        self.praiseLabel.move(430, 50)

        self.praiseText = QPlainTextEdit(self)
        self.praiseText.setReadOnly(True)
        self.praiseText.setFixedSize(QSize(160, 200))
        self.praiseText.move(430, 80)

    def initBackButton(self):
        self.backButton = QPushButton("Back", self)
        self.backButton.setFixedSize(QSize(80, 30))
        self.backButton.move(510, 290)
        self.backButton.clicked.connect(self.backButtonClicked)

    def updateEvaluationList(self):
        g_evaluation_list.clear()
        self.evaluationList.clear()
        api = Api()
        response = api.get_all_evaluation()
        if response.json()["message"] == "not found":
            return
        if response.json()["message"] != "success":
            QMessageBox.warning(self, "Warning", response.json()["data"])
            return
        evaluation_list = response.json()["data"]
        for evaluation in evaluation_list:
            course_id = evaluation['courseId']
            course_response = api.get_course_by_id(course_id)
            if course_response.json()['message'] != 'success':
                QMessageBox.warning(
                    self, "Error", course_response.json()['data'])
                return
            course = course_response.json()['data']
            student_id = evaluation['studentId']
            student_response = api.get_student_by_id(student_id)
            if student_response.json()['message'] != 'success':
                QMessageBox.warning(
                    self, "Error", student_response.json()['data'])
                return
            student = student_response.json()['data']
            g_evaluation_list.append(evaluation)
            self.evaluationList.insertItem(
                evaluation["id"], course["title"] + " - " + student["name"])

    def updateQuestionList(self, evaluation_id):
        g_question_list.clear()
        self.questionList.clear()
        api = Api()
        response = api.get_all_question_by_evaluation_id(evaluation_id)
        if response.json()["message"] == "not found":
            return
        if response.json()["message"] != "success":
            QMessageBox.warning(self, "Warning", response.json()["data"])
            return
        question_list = response.json()["data"]
        for question in question_list:
            g_question_list.append(question)
            self.questionList.insertItem(
                question["id"], question["content"])

    @pyqtSlot()
    def courseNewButtonClicked(self):
        self.createEvaluationWindow = CreateEvaluationWindow(self)
        self.createEvaluationWindow.show()

    @pyqtSlot()
    def evaluationListClicked(self):
        evaluation_index = self.evaluationList.currentRow()
        evaluation_id = g_evaluation_list[evaluation_index]["id"]
        self.updateQuestionList(evaluation_id)

    @pyqtSlot()
    def questionListClicked(self):
        index = self.questionList.currentRow()
        question_id = g_question_list[index]["id"]
        api = Api()
        response = api.get_question_by_id(question_id)
        if response.json()["message"] != "success":
            QMessageBox.warning(self, "Warning", response.json()["data"])
            return
        question = response.json()["data"]
        self.markValue.setValue(question["score"])
        evaluation_id = g_question_list[index]["evaluationId"]
        praise_response = api.get_praise_by_evaluation_id(evaluation_id)
        if praise_response.json()['message'] != 'success':
            QMessageBox.warning(
                self, "Error", praise_response.json()['data'])
            return
        praise = praise_response.json()['data']
        self.praiseText.setPlainText(praise["content"])

    @pyqtSlot()
    def backButtonClicked(self) -> None:
        self.close()
        self.father.show()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
