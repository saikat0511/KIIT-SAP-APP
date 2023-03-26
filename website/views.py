from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user
from .attendance import get_attendance
from .models import User


views = Blueprint('views', __name__)

@views.route('/')
@login_required
def home():
    return render_template('home.html', user=current_user)


@views.route('/get_attendance/', methods=['POST'])
def get_attendance_response():
    data = request.get_json()
    user = User.query.filter_by(id=data.get('user')).first()
    id = user.id
    password = user.password
    year = data.get('year')
    session = data.get('session')
    attendance = get_attendance(id, password, year, session)
    #print(attendance)
    return jsonify(attendance)
