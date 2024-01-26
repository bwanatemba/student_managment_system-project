# app/models.py
from flask_login import UserMixin
from werkzeug.security import generate_password_hash
import random


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer)
    national_id = db.Column(db.String(20), unique=True, nullable=False)
    faculty = db.Column(db.String(50), nullable=False)
    program = db.Column(db.String(50), nullable=False)
    student_number = db.Column(db.String(20), unique=True, nullable=False)

    def __init__(self, name, age, national_id, faculty, program):
        self.name = name
        self.age = age
        self.national_id = national_id
        self.faculty = faculty
        self.program = program
        self.student_number = generate_student_number()  # Implement this function

    def generate_student_number():
    return str(random.randint(1000000000, 9999999999))


class Receipt(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    amount_paid = db.Column(db.Float, nullable=False)

    def __init__(self, student_id, amount_paid):
        self.student_id = student_id
        self.amount_paid = amount_paid


class Faculty(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
