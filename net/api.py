#!/usr/env/bin python3
# -*- coding: utf-8 -*-
# Author: Aimer Neige
# Mail: aimer.neige@aimerneige.com
# LICENSE: AGPLv3 (https://www.gnu.org/licenses/agpl-3.0.txt)


import requests
from requests.models import Response
from requests.sessions import Session

base_url = 'https://tencent.aimerneige.com:21911/course_evaluation'

s = Session()


class Api():

    def __init__(self):
        self.root = base_url
        self.admin_url = self.root + '/admin'
        self.course_url = self.root + '/course'
        self.evaluation_url = self.root + '/evaluation'
        self.praise_url = self.root + '/praise'
        self.question_url = self.root + '/question'
        self.student_url = self.root + '/student'
        self.teacher_url = self.root + '/teacher'
        self.mail_url = self.root + '/mail'

    def get_all_admin(self):
        response = requests.get(self.admin_url)
        return response

    def create_new_admin(self, name, username, password):
        data = {
            'name': name,
            'username': username,
            'password': password
        }
        response = requests.post(self.admin_url, json=data)
        return response

    def get_admin_by_id(self, id):
        response = requests.get(self.admin_url + '/' + str(id))
        return response

    def update_admin_by_id(self, id, name, username, password):
        data = {
            'name': name,
            'username': username,
            'password': password
        }
        response = requests.put(self.admin_url + '/' + str(id), json=data)
        return response

    def delete_admin(self, id):
        response = requests.delete(self.admin_url + '/' + str(id))
        return response

    def search_admin_by_name(self, name):
        response = requests.get(
            self.admin_url + '/search', params={'name': name})
        return response

    def admin_login(self, username, password):
        response = requests.get(
            self.admin_url + '/login',
            params={'username': username, 'password': password})
        return response

    def get_all_course(self):
        response = requests.get(self.course_url)
        return response

    def create_new_course(self, title, description, teacher_id):
        data = {
            "title": title,
            "description": description,
            "teacherId": teacher_id
        }
        response = requests.post(self.course_url, json=data)
        return response

    def get_course_by_id(self, id):
        response = requests.get(self.course_url + '/' + str(id))
        return response

    def update_course_by_id(self, id, title, description, teacher_id):
        data = {
            "title": title,
            "description": description,
            "teacherId": teacher_id
        }
        response = requests.put(self.course_url + '/' + str(id), json=data)
        return response

    def delete_course_by_id(self, id):
        response = requests.delete(self.course_url + '/' + str(id))
        return response

    def get_all_students_by_course_id(self, course_id):
        response = requests.get(
            self.course_url + '/' + str(course_id) + '/students')
        return response

    def add_student_to_course(self, course_id, student_id):
        response = requests.post(
            self.course_url + '/' + str(course_id) + '/student', params={'studentId': student_id})
        return response

    def delete_student_from_course(self, course_id, student_id):
        response = requests.delete(
            self.course_url + '/' + str(course_id) + '/student', params={'studentId': student_id})
        return response

    def search_course_by_title(self, title):
        response = requests.get(
            self.course_url + '/search', params={'title': title})
        return response

    def get_all_course_by_teacher_id(self, teacher_id):
        response = requests.get(
            self.course_url + '/teacher', params={'teacherId': teacher_id})
        return response

    def get_all_evaluation(self):
        response = requests.get(self.evaluation_url)
        return response

    def create_new_evaluation(self, student_id, course_id):
        data = {
            "studentId": student_id,
            "courseId": course_id
        }
        response = requests.post(self.evaluation_url, json=data)
        return response

    def get_evaluation_by_id(self, id):
        response = requests.get(self.evaluation_url + '/' + str(id))
        return response

    def update_evaluation_by_id(self, id, student_id, course_id):
        data = {
            "studentId": student_id,
            "courseId": course_id
        }
        response = requests.put(self.evaluation_url + '/' + str(id), json=data)
        return response

    def delete_evaluation_by_id(self, id):
        response = requests.delete(self.evaluation_url + '/' + str(id))
        return response

    def get_all_evaluation_by_student_id(self, student_id):
        response = requests.get(
            self.evaluation_url + '/student/', params={'studentId': student_id})
        return response

    def get_all_evaluation_by_course_id(self, course_id):
        response = requests.get(
            self.evaluation_url + '/course/', params={'courseId': course_id})
        return response

    def get_all_praise(self):
        response = requests.get(self.praise_url)
        return response

    def create_new_praise(self, content, evaluation_id):
        data = {
            "content": content,
            "evaluationId": evaluation_id
        }
        response = requests.post(self.praise_url, json=data)
        return response

    def get_praise_by_id(self, id):
        response = requests.get(self.praise_url + '/' + str(id))
        return response

    def update_praise_by_id(self, id, content, evaluation_id):
        data = {
            "content": content,
            "evaluationId": evaluation_id
        }
        response = requests.put(self.praise_url + '/' + str(id), json=data)
        return response

    def delete_praise_by_id(self, id):
        response = requests.delete(self.praise_url + '/' + str(id))
        return response

    def get_praise_by_evaluation_id(self, evaluation):
        response = requests.get(
            self.praise_url + '/evaluation', params={'evaluationId': evaluation})
        return response

    def get_all_question(self):
        response = requests.get(self.question_url)
        return response

    def create_new_question(self, content, score, evaluation_id):
        data = {
            "content": content,
            "score": score,
            "evaluationId": evaluation_id
        }
        response = requests.post(self.question_url, json=data)
        return response

    def get_question_by_id(self, id):
        response = requests.get(self.question_url + '/' + str(id))
        return response

    def update_question_by_id(self, id, content, score, evaluation_id):
        data = {
            "content": content,
            "score": score,
            "evaluationId": evaluation_id
        }
        response = requests.put(self.question_url + '/' + str(id), json=data)
        return response

    def delete_question_by_id(self, id):
        response = requests.delete(self.question_url + '/' + str(id))
        return response

    def get_all_question_by_evaluation_id(self, evaluation_id):
        response = requests.get(
            self.question_url + '/evaluation', params={'evaluationId': evaluation_id})
        return response

    def get_all_student(self):
        response = requests.get(self.student_url)
        return response

    def create_new_student(self, id_number, name, phone, sex, email, password, age):
        data = {
            "idNumber": id_number,
            "name": name,
            "phone": phone,
            "sex": sex,
            "email": email,
            "password": password,
            "age": age
        }
        response = s.post(self.student_url, json=data)
        return response

    def register_new_student(self, id_number, name, phone, sex, email, password, age, verify_code):
        data = {
            "idNumber": id_number,
            "name": name,
            "phone": phone,
            "sex": sex,
            "email": email,
            "password": password,
            "age": age,
            "verifyCode": verify_code
        }
        response = s.post(self.student_url + '/register', json=data)
        return response

    def get_student_by_id(self, id):
        response = requests.get(self.student_url + '/' + str(id))
        return response

    def update_student_by_id(self, id, id_number, name, phone, sex, email, password, age):
        data = {
            "idNumber": id_number,
            "name": name,
            "phone": phone,
            "sex": sex,
            "email": email,
            "password": password,
            "age": age
        }
        response = requests.put(self.student_url + '/' + str(id), json=data)
        return response

    def delete_student_by_id(self, id):
        response = requests.delete(self.student_url + '/' + str(id))
        return response

    def search_student_by_name(self, name):
        response = requests.get(
            self.student_url + '/search', params={'name': name})
        return response

    def student_login(self, id_number, password):
        response = requests.get(
            self.student_url + '/login', params={'idNumber': id_number, 'password': password})
        return response

    def get_all_teacher(self):
        response = requests.get(self.teacher_url)
        return response

    def create_new_teacher(self, id_number, name, phone, sex, age):
        data = {
            'idNumber': id_number,
            "name": name,
            "phone": phone,
            "sex": sex,
            "age": age
        }
        response = requests.post(self.teacher_url, json=data)
        return response

    def get_teacher_by_id(self, id):
        response = requests.get(self.teacher_url + '/' + str(id))
        return response

    def update_teacher(self, id, id_number, name, phone, sex, age):
        data = {
            'idNumber': id_number,
            "name": name,
            "phone": phone,
            "sex": sex,
            "age": age
        }
        response = requests.put(self.teacher_url, json=data)
        return response

    def delete_teacher_by_id(self, id):
        response = requests.delete(self.teacher_url + '/' + str(id))
        return response

    def search_teacher_by_name(self, name):
        response = requests.get(
            self.teacher_url + '/search', params={'name': name})
        return response

    def send_verify_mail(self, to):
        data = {
            "to": to
        }
        response = s.post(self.mail_url, json=data)
        return response
