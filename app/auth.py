# app/auth.py
from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash
from .models import User
from .utils import is_admin

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('auth/login.html')


@auth_bp.route('/logout')
@login_required
def logout():
    # Logic for user logout
    return redirect(url_for('auth.login'))

