from flask import Blueprint, render_template, request, jsonify
from .attendance import get_attendance
from .login import is_valid_user


views = Blueprint('views', __name__)

@views.route('/')
def home():
    return render_template('home.html')


@views.route('/get_attendance/', methods=['POST'])
def get_attendance_response():
    data = request.get_json()
    userid = data.get('userid')
    password = data.get('password')
    year = data.get('year')
    session = data.get('session')
    attendance = get_attendance(userid, password, year, session)
    #print(attendance)
    return jsonify(attendance)


@views.route('/check_id/', methods=['POST'])
def check_id():
    data = request.get_json()
    userid = data.get('userid')
    password = data.get('password')
    return str(is_valid_user(userid, password))
