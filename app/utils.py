from functools import wraps
from flask import flash, redirect, url_for
from flask_login import current_user
import random
from PIL import Image, ImageDraw, ImageFont
import os


def is_admin(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            flash('Permission denied. Admins only.', 'danger')
            return redirect(url_for('auth.login'))
        return func(*args, **kwargs)

    return wrapper


def generate_student_id_card(student):
    template_path = 'path/to/template/image.jpg'
    if not os.path.exists(template_path):
        raise FileNotFoundError(f"Template image not found at {template_path}")
    output_path = f'static/id_cards/{student.student_number}_id_card.jpg'

    img = Image.open(template_path)
    draw = ImageDraw.Draw(img)
    font = ImageFont.load_default()

    draw.text((10, 10), f"Student Name: {student.name}", (0, 0, 0), font=font)
    draw.text((10, 30), f"Student Number: {student.student_number}", (0, 0, 0), font=font)

    img.save(output_path)


def generate_student_number():
    return str(random.randint(1000000000, 9999999999))
