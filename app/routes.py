from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from .models import Student, Receipt
from .utils import is_admin
import os
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from .models import Student
from .utils import is_admin, generate_student_id_card
from . import db

student_bp = Blueprint('student', __name__, url_prefix='/student')


@student_bp.route('/')
@login_required
def student_dashboard():
    return render_template('student/dashboard.html', student=current_user)


@student_bp.route('/register', methods=['GET', 'POST'])
@login_required
def register_student():
    if request.method == 'POST':
        name = request.form.get('name')
        age = int(request.form.get('age'))
        national_id = request.form.get('national_id')
        faculty = request.form.get('faculty')
        program = request.form.get('program')

        new_student = Student(name=name, age=age, national_id=national_id, faculty=faculty, program=program)
        db.session.add(new_student)
        db.session.commit()

        flash('Student registered successfully!', 'success')
        return redirect(url_for('student.student_dashboard'))

    return render_template('student/register.html')


@student_bp.route('/generate_id_card')
@login_required
def generate_id_card():
    generate_student_id_card(current_user)

    flash('Student ID card generated successfully!', 'success')
    return redirect(url_for('student.student_dashboard'))


receipt_bp = Blueprint('receipt', __name__, url_prefix='/receipt')


@receipt_bp.route('/issue', methods=['GET', 'POST'])
@login_required
@is_admin
def issue_receipt():
    if request.method == 'POST':
        student_id = int(request.form.get('student_id'))
        amount_paid = float(request.form.get('amount_paid'))

        new_receipt = Receipt(student_id=student_id, amount_paid=amount_paid)
        db.session.add(new_receipt)
        db.session.commit()

        flash('Receipt issued successfully!', 'success')
        return redirect(url_for('receipt.issue_receipt'))

    students = Student.query.all()
    receipts = Receipt.query.all()

    return render_template('receipt/issue_receipt.html', students=students, receipts=receipts)
