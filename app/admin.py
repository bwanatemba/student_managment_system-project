# app/admin.py
from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required
from .utils import is_admin
from .models import Faculty


admin_bp = Blueprint('admin', __name__, url_prefix='/admin')


@admin_bp.route('/')
@login_required
@is_admin
def admin_dashboard():
    faculties = Faculty.query.all()
    return render_template('admin/dashboard.html', faculties=faculties)


@admin_bp.route('/add_faculty', methods=['GET', 'POST'])
@login_required
@is_admin
def add_faculty():
    if request.method == 'POST':
        faculty_name = request.form.get('faculty_name')

        if not faculty_name:
            flash('Faculty name is required.', 'danger')
            return redirect(url_for('admin.add_faculty'))

        new_faculty = Faculty(name=faculty_name)
        db.session.add(new_faculty)
        db.session.commit()

        flash('Faculty added successfully!', 'success')
        return redirect(url_for('admin.add_faculty'))

    return render_template('admin/add_faculty.html')

@admin_bp.route('/edit_faculty/<int:faculty_id>', methods=['GET', 'POST'])
@login_required
@is_admin
def edit_faculty(faculty_id):
    faculty = Faculty.query.get_or_404(faculty_id)

    if request.method == 'POST':
        faculty.name = request.form.get('faculty_name')

        if not faculty.name:
            flash('Faculty name is required.', 'danger')
            return redirect(url_for('admin.edit_faculty', faculty_id=faculty.id))

        db.session.commit()
        flash('Faculty updated successfully!', 'success')
        return redirect(url_for('admin.admin_dashboard'))

    return render_template('admin/edit_faculty.html', faculty=faculty)
