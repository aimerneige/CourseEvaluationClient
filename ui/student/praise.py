#!/usr/env/bin python3
# -*- coding: utf-8 -*-
# Author: Aimer Neige
# Mail: aimer.neige@aimerneige.com
# LICENSE: AGPLv3 (https://www.gnu.org/licenses/agpl-3.0.txt)

import json

from PyQt5.QtCore import QSize, pyqtSlot
from PyQt5.QtWidgets import QDesktopWidget, QLabel, QMainWindow, QMessageBox, QPlainTextEdit, QPushButton, QSpinBox

from net.api import Api


window_title = "Student Praise"
window_width = 300
window_height = 180


class StudentPraiseWindow(QMainWindow):
    def __init__(self, father):
        super().__init__()
        self.father = father
        self.evaluationId = father.evaluationId
        self.initWindow()
        self.initUI()
        self.center()

    def initWindow(self):
        self.setWindowTitle(window_title)
        self.setFixedWidth(window_width)
        self.setFixedHeight(window_height)

    def initUI(self):
        self.initPraiseWidgets()
        self.initButton()

    def initPraiseWidgets(self):
        self.praiseLabel = QLabel("Praise:", self)
        self.praiseLabel.setFixedSize(QSize(280, 40))
        self.praiseLabel.move(10, 10)

        self.praiseInput = QPlainTextEdit(self)
        self.praiseInput.setFixedSize(QSize(280, 80))
        self.praiseInput.setReadOnly(False)
        self.praiseInput.move(10, 50)

    def initButton(self):
        self.submitButton = QPushButton("Submit", self)
        self.submitButton.setFixedSize(QSize(100, 30))
        self.submitButton.move(10, 140)
        self.submitButton.clicked.connect(self.submitButtonClicked)

    @pyqtSlot()
    def submitButtonClicked(self):
        content = self.praiseInput.toPlainText()
        evaluation_id = self.evaluationId
        api = Api()
        response = api.create_new_praise(content, evaluation_id)
        if response.json()['message'] != 'success':
            QMessageBox.warning(self, "Warning", response.json()['message'])
            return
        self.close()
        self.father.show()
        self.father.updateEvaluationData()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
