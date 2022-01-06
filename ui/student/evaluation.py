#!/usr/env/bin python3
# -*- coding: utf-8 -*-
# Author: Aimer Neige
# Mail: aimer.neige@aimerneige.com
# LICENSE: AGPLv3 (https://www.gnu.org/licenses/agpl-3.0.txt)


from PyQt5.QtCore import QSize, pyqtSlot
from PyQt5.QtWidgets import QDesktopWidget, QMainWindow, QPushButton


window_title = "Evaluation Question"
window_width = 300
window_height = 140

button_size = QSize(100, 30)


class StudentEvaluationWindow(QMainWindow):
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
        self.backButton = QPushButton("Back", self)
        self.backButton.setFixedSize(button_size)
        self.backButton.move(100, 50)
        self.backButton.clicked.connect(self.backButtonClicked)

    def updateUI(self):
        self.evaluationId = self.father.evaluationId

    @pyqtSlot()
    def backButtonClicked(self) -> None:
        self.close()
        self.father.show()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
