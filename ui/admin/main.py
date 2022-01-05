#!/usr/env/bin python3
# -*- coding: utf-8 -*-
# Author: Aimer Neige
# Mail: aimer.neige@aimerneige.com
# LICENSE: AGPLv3 (https://www.gnu.org/licenses/agpl-3.0.txt)


from PyQt5.QtWidgets import QMainWindow


window_title = "Admin Manage"
window_width = 300
window_height = 140


class AdminMainWindow(QMainWindow):
    def __init__(self, father) -> None:
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
        pass
