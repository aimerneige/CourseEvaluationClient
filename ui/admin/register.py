#!/usr/env/bin python3
# -*- coding: utf-8 -*-
# Author: Aimer Neige
# Mail: aimer.neige@aimerneige.com
# LICENSE: AGPLv3 (https://www.gnu.org/licenses/agpl-3.0.txt)


from PyQt5.QtWidgets import QDesktopWidget, QMainWindow


window_title = "Admin Register"
window_width = 300
window_height = 140


class AdminRegisterWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.initWindow()
        self.initUI()
        self.center()

    def initWindow(self) -> None:
        """
        Init window properties.
        """
        self.setWindowTitle(window_title)
        self.setFixedWidth(window_width)
        self.setFixedHeight(window_height)

    def initUI(self) -> None:
        """
        Init UI widgets and layout.
        """
        pass

    def center(self) -> None:
        """
        Center the window on the screen.
        """
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
