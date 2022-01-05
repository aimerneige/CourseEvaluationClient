#!/usr/env/bin python3
# -*- coding: utf-8 -*-
# Author: Aimer Neige
# Mail: aimer.neige@aimerneige.com
# LICENSE: AGPLv3 (https://www.gnu.org/licenses/agpl-3.0.txt)


from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QDesktopWidget, QPushButton, QWidget


class AdminLogin(QWidget):
    def __init__(self, father) -> None:
        super().__init__()
        self.father = father
        self.setFixedSize(300, 200)
        self.initUI()
        self.center()

    def initUI(self) -> None:
        self.backBtn = QPushButton('Back', self)
        self.backBtn.clicked.connect(self.back)

    @pyqtSlot()
    def back(self) -> None:
        self.close()
        self.father.show()

    def center(self) -> None:
        """
        Center the window on the screen.
        """
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
