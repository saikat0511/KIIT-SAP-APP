from flask import Blueprint, render_template, request, flash
from flask_login import login_required, current_user
from .attendance import get_attendance


views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        year = str(request.form.get('year'))
        session = str(request.form.get('session'))
        attendance = get_attendance(current_user.id, 
                                    current_user.password, 
                                    year, 
                                    session)
        if attendance == -1:
            flash('SAP is unreachable', category='error')
            return render_template('home.html', user=current_user)
        return render_template('home_attendance.html', 
                               user=current_user, 
                               attendance=attendance, 
                               len=len(attendance['Subject']), 
                               col_list = list(attendance.keys()))
    elif request.method == 'GET':
        return render_template('home.html', user=current_user)


@views.route('/', methods=['POST'])
def is_valid_user():
    if request.method == 'POST':
        print(request.get_json())
