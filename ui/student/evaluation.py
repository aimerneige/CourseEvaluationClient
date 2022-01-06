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

question_content_list = [
    "PPT 的设计与制作",
    "教学工具",
    "教材及参考资料",
    "教案",
    "PPT的使用与板书",
    "为人师表",
    "学生出勤与课堂纪律",
    "对课堂的把控能力",
    "教学方法",
    "案例教学或习题课",
    "讲授内容",
    "讲授进度",
    "语言表达",
    "课程思政",
    "持续改进",
    "辅导答疑",
    "作业内容",
    "作业布置",
    "作业批改",
    "考核内容",
    "考核方式"
]


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
