#!/usr/env/bin python3
# -*- coding: utf-8 -*-
# Author: Aimer Neige
# Mail: aimer.neige@aimerneige.com
# LICENSE: AGPLv3 (https://www.gnu.org/licenses/agpl-3.0.txt)


from PyQt5.QtCore import QSize, pyqtSlot
from PyQt5.QtWidgets import QComboBox, QDesktopWidget, QLabel, QListWidget, QMainWindow, QMessageBox, QPlainTextEdit, QPushButton, QLineEdit

from net.api import Api
from ui.admin.course.student import InsertStudentWindow


window_title = "Course Manage"
window_width = 720
window_height = 300

g_course_list = []
g_teacher_list = []
g_student_list = []


class CourseMainWindow(QMainWindow):
    def __init__(self, father):
        super().__init__()
        self.father = father
        self.courseId = 0
        self.initWindow()
        self.initUI()
        self.center()
        self.updateUI()

    def initWindow(self):
        self.setWindowTitle(window_title)
        self.setFixedWidth(window_width)
        self.setFixedHeight(window_height)

    def initUI(self):
        self.initSearchWidgets()
        self.initCourseInfoWidgets()
        self.initStudentWidgets()

    def updateUI(self):
        self.updateCourseData()
        self.updateTeacherData()

    def initSearchWidgets(self):
        self.searchInput = QLineEdit(self)
        self.searchInput.setFixedSize(QSize(100, 30))
        self.searchInput.move(10, 10)

        self.searchButton = QPushButton("Search", self)
        self.searchButton.setFixedSize(QSize(70, 30))
        self.searchButton.move(120, 10)
        self.searchButton.clicked.connect(self.searchButtonClicked)

        self.courseList = QListWidget(self)
        self.courseList.setFixedSize(QSize(180, 200))
        self.courseList.move(10, 50)
        self.courseList.clicked.connect(self.courseListClicked)

        self.resetButton = QPushButton("Reset", self)
        self.resetButton.setFixedSize(QSize(85, 30))
        self.resetButton.move(10, 260)
        self.resetButton.clicked.connect(self.resetButtonClicked)

        self.clearButton = QPushButton("Clear", self)
        self.clearButton.setFixedSize(QSize(85, 30))
        self.clearButton.move(105, 260)
        self.clearButton.clicked.connect(self.clearButtonClicked)

    def initCourseInfoWidgets(self):
        self.titleLabel = QLabel("Title:", self)
        self.titleLabel.setFixedSize(QSize(80, 20))
        self.titleLabel.move(200, 10)

        self.titleInput = QLineEdit(self)
        self.titleInput.setFixedSize(QSize(260, 30))
        self.titleInput.move(200, 40)

        self.descriptionLabel = QLabel("Description:", self)
        self.descriptionLabel.setFixedSize(QSize(80, 20))
        self.descriptionLabel.move(200, 80)

        self.descriptionInput = QPlainTextEdit(self)
        self.descriptionInput.setFixedSize(QSize(260, 60))
        self.descriptionInput.move(200, 110)

        self.teacherLabel = QLabel("Teacher:", self)
        self.teacherLabel.setFixedSize(QSize(80, 20))
        self.teacherLabel.move(200, 180)

        self.teacherComb = QComboBox(self)
        self.teacherComb.setFixedSize(QSize(260, 30))
        self.teacherComb.move(200, 220)

        self.newButton = QPushButton("New", self)
        self.newButton.setFixedSize(QSize(80, 30))
        self.newButton.move(200, 260)
        self.newButton.clicked.connect(self.newButtonClicked)

        self.saveButton = QPushButton("Save", self)
        self.saveButton.setFixedSize(QSize(80, 30))
        self.saveButton.move(290, 260)
        self.saveButton.clicked.connect(self.saveButtonClicked)

        self.deleteButton = QPushButton("Delete", self)
        self.deleteButton.setFixedSize(QSize(80, 30))
        self.deleteButton.move(380, 260)
        self.deleteButton.clicked.connect(self.deleteButtonClicked)

    def initStudentWidgets(self):
        self.studentLabel = QLabel("Students:", self)
        self.studentLabel.setFixedSize(QSize(80, 20))
        self.studentLabel.move(470, 10)

        self.studentList = QListWidget(self)
        self.studentList.setFixedSize(QSize(240, 210))
        self.studentList.move(470, 40)

        self.studentNewButton = QPushButton("New", self)
        self.studentNewButton.setFixedSize(QSize(70, 30))
        self.studentNewButton.move(470, 260)
        self.studentNewButton.clicked.connect(self.studentNewButtonClicked)

        self.studentDeleteButton = QPushButton("Delete", self)
        self.studentDeleteButton.setFixedSize(QSize(70, 30))
        self.studentDeleteButton.move(550, 260)
        self.studentDeleteButton.clicked.connect(
            self.studentDeleteButtonClicked)

        self.backButton = QPushButton("Back", self)
        self.backButton.setFixedSize(QSize(70, 30))
        self.backButton.move(640, 260)
        self.backButton.clicked.connect(self.backButtonClicked)

    def updateCourseData(self):
        g_course_list.clear()
        self.courseList.clear()
        api = Api()
        response = api.get_all_course()
        if response.json()['message'] != 'success':
            QMessageBox.warning(self, "Error", response.json()['data'])
            return
        course_list = response.json()['data']
        for course in course_list:
            g_course_list.append(course)
            self.courseList.insertItem(course['id'], course['title'])

    def updateTeacherData(self):
        g_teacher_list.clear()
        self.teacherComb.clear()
        api = Api()
        response = api.get_all_teacher()
        if response.json()['message'] != 'success':
            QMessageBox.warning(self, "Error", response.json()['data'])
            return
        teacher_list = response.json()['data']
        for teacher in teacher_list:
            g_teacher_list.append(teacher)
            self.teacherComb.insertItem(teacher['id'], teacher['name'])
        self.teacherComb.setCurrentIndex(-1)

    def updateStudentData(self):
        g_student_list.clear()
        self.studentList.clear()
        course_index = self.courseList.currentRow()
        course_id = g_course_list[course_index]['id']
        api = Api()
        response = api.get_all_students_by_course_id(course_id)
        if response.json()['message'] != 'success':
            QMessageBox.warning(self, "Error", response.json()['data'])
            return
        student_list = response.json()['data']
        for student in student_list:
            g_student_list.append(student)
            self.studentList.insertItem(student['id'], student['name'])

    @pyqtSlot()
    def courseListClicked(self):
        index = self.courseList.currentRow()
        course_id = g_course_list[index]['id']
        self.courseId = course_id
        api = Api()
        response = api.get_course_by_id(course_id)
        if response.json()['message'] != 'success':
            QMessageBox.warning(self, "Error", response.json()['data'])
            return
        data = response.json()['data']
        title = data['title']
        self.titleInput.setText(title)
        description = data['description']
        self.descriptionInput.setPlainText(description)
        teacher_id = data['teacherId']
        index = 0
        for teacher in g_teacher_list:
            if teacher['id'] == teacher_id:
                self.teacherComb.setCurrentIndex(index)
                break
            index += 1
        self.updateStudentData()

    @pyqtSlot()
    def searchButtonClicked(self):
        keyword = self.searchInput.text()
        if keyword == '':
            QMessageBox.warning(self, "Error", "Please input search keyword.")
            return
        api = Api()
        response = api.search_course_by_title(keyword)
        if response.json()['message'] != 'success':
            QMessageBox.warning(self, "Error", response.json()['data'])
            return
        course_list = response.json()['data']
        g_course_list.clear()
        self.courseList.clear()
        for course in course_list:
            g_course_list.append(course)
            self.courseList.insertItem(course['id'], course['title'])

    @pyqtSlot()
    def resetButtonClicked(self):
        self.searchInput.setText('')
        self.updateCourseData()

    @pyqtSlot()
    def clearButtonClicked(self):
        self.titleInput.setText('')
        self.descriptionInput.setPlainText('')
        self.teacherComb.setCurrentIndex(-1)

    @pyqtSlot()
    def newButtonClicked(self):
        title = self.titleInput.text()
        description = self.descriptionInput.toPlainText()
        teacher_id = g_teacher_list[self.teacherComb.currentIndex()]['id']
        if title == '':
            QMessageBox.warning(self, "Error", "Please input title.")
            return
        if description == '':
            QMessageBox.warning(self, "Error", "Please input description.")
            return
        if self.teacherComb.currentIndex() == -1:
            QMessageBox.warning(self, "Error", "Please select a teacher.")
            return
        api = Api()
        response = api.create_new_course(title, description, teacher_id)
        if response.json()['message'] != 'success':
            QMessageBox.warning(self, "Error", response.json()['data'])
            return
        QMessageBox.information(
            self, "Success", "Create new course successfully.")
        self.updateCourseData()

    @pyqtSlot()
    def saveButtonClicked(self):
        course_index = self.courseList.currentRow()
        course_id = g_course_list[course_index]['id']
        title = self.titleInput.text()
        description = self.descriptionInput.toPlainText()
        teacher_index = self.teacherComb.currentIndex()
        teacher_id = g_teacher_list[teacher_index]['id']
        api = Api()
        response = api.update_course_by_id(
            course_id, title, description, teacher_id)
        if response.json()['message'] != 'success':
            QMessageBox.warning(self, "Error", response.json()['data'])
            return
        QMessageBox.information(
            self, "Success", "Save New Course Successfully.")
        self.updateUI()

    @pyqtSlot()
    def deleteButtonClicked(self):
        course_index = self.courseList.currentRow()
        course_id = g_course_list[course_index]['id']
        api = Api()
        response = api.delete_course_by_id(course_id)
        if response.json()['message'] != 'success':
            QMessageBox.warning(self, "Error", response.json()['data'])
            return
        QMessageBox.information(
            self, "Success", "Delete Course Successfully.")
        self.updateUI()

    @pyqtSlot()
    def studentNewButtonClicked(self):
        self.insertStudentWindow = InsertStudentWindow(self)
        self.insertStudentWindow.show()

    @pyqtSlot()
    def studentDeleteButtonClicked(self):
        course_index = self.courseList.currentRow()
        course_id = g_course_list[course_index]['id']
        student_index = self.studentList.currentRow()
        student_id = g_student_list[student_index]['id']
        api = Api()
        response = api.delete_student_from_course(course_id, student_id)
        if response.json()['message'] != 'success':
            QMessageBox.warning(self, "Error", response.json()['data'])
            return
        QMessageBox.information(
            self, "Success", "Delete student successfully.")
        self.updateStudentData()

    @pyqtSlot()
    def backButtonClicked(self):
        self.close()
        self.father.show()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
