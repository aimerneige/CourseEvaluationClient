#!/usr/env/bin python3
# -*- coding: utf-8 -*-
# Author: Aimer Neige
# Mail: aimer.neige@aimerneige.com
# LICENSE: AGPLv3 (https://www.gnu.org/licenses/agpl-3.0.txt)

import json

from PyQt5.QtCore import QSize, pyqtSlot
from PyQt5.QtWidgets import QDesktopWidget, QLabel, QMainWindow, QMessageBox, QPlainTextEdit, QPushButton, QSpinBox

from net.api import Api
from ui.student.praise import StudentPraiseWindow


window_title = "Student Question"
window_width = 300
window_height = 220


class StudentQuestionWindow(QMainWindow):
    def __init__(self, father):
        super().__init__()
        self.father = father
        self.evaluationId = father.evaluationId
        self.question_list = []
        self.question_index = 0
        self.initWindow()
        self.initUI()
        self.updateUI()
        self.center()

    def initWindow(self):
        self.setWindowTitle(window_title)
        self.setFixedWidth(window_width)
        self.setFixedHeight(window_height)

    def initUI(self):
        self.initQuestionWidgets()
        self.initButton()

    def initQuestionWidgets(self):
        self.questionTitle = QLabel(self)
        self.questionTitle.setFixedSize(QSize(280, 40))
        self.questionTitle.move(10, 10)

        self.questionDetail = QPlainTextEdit(self)
        self.questionDetail.setFixedSize(QSize(280, 80))
        self.questionDetail.setReadOnly(True)
        self.questionDetail.move(10, 50)

        self.scoreLabel = QLabel("Score:", self)
        self.scoreLabel.setFixedSize(QSize(80, 30))
        self.scoreLabel.move(10, 140)

        self.scoreValue = QSpinBox(self)
        self.scoreValue.setReadOnly(False)
        self.scoreValue.setMaximum(100)
        self.scoreValue.setMinimum(0)
        self.scoreValue.setValue(100)
        self.scoreValue.setFixedSize(QSize(80, 30))
        self.scoreValue.move(100, 140)

    def initButton(self):
        self.submitButton = QPushButton("Submit", self)
        self.submitButton.setFixedSize(QSize(100, 30))
        self.submitButton.move(10, 180)
        self.submitButton.clicked.connect(self.submitButtonClicked)

        self.finishButton = QPushButton("Finish", self)
        self.finishButton.setFixedSize(QSize(100, 30))
        self.finishButton.move(190, 180)
        self.finishButton.clicked.connect(self.finishButtonClicked)
        self.finishButton.hide()

    def updateUI(self):
        self.readQuestionsFromJsonFile()
        self.questionTitle.setText(
            self.question_list[self.question_index]['title'])
        self.questionDetail.setPlainText(
            self.question_list[self.question_index]['detail'])

    def readQuestionsFromJsonFile(self):
        with open("question.json", "r") as f:
            self.question_list = json.load(f)['data']

    @pyqtSlot()
    def submitButtonClicked(self):
        content = self.questionTitle.text()
        score = self.scoreValue.value()
        evaluation_id = self.evaluationId
        api = Api()
        response = api.create_new_question(content, score, evaluation_id)
        if response.json()['message'] != 'success':
            QMessageBox.warning(self, "Error", response.json()['data'])
            return
        if len(self.question_list) == self.question_index + 1:
            self.submitButton.hide()
            self.finishButton.show()
        else:
            self.question_index += 1
            self.updateUI()

    @pyqtSlot()
    def finishButtonClicked(self):
        self.close()
        self.studentPraiseWindow = StudentPraiseWindow(self.father)
        self.studentPraiseWindow.show()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
