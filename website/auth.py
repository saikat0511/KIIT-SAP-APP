from flask import Blueprint, render_template, request, redirect, url_for
from .login import is_valid_user
from .models import User
from . import db
from flask_login import login_user, logout_user, login_required, current_user

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('views.home'))
    if request.method == 'POST':
        uid = str(request.form.get('uid'))
        password = str(request.form.get('password'))

        if is_valid_user(uid, password) == False:
            message = 'Invalid User ID/Password, or SAP is unreachable'
            return render_template('login.html', user=current_user, message=message, len=len(message))
        else:
            # add user to database if not present, then login
            user = User.query.filter_by(id=uid).first()
            if not user:
                new_user = User(id=uid, password=password)
                db.session.add(new_user)
                db.session.commit()
                login_user(new_user, remember=True)
            else:
                login_user(user, remember=True)
            #print(User.query.get(password))
            return redirect(url_for('views.home'))
    if request.method == 'GET':
        return render_template('login.html', user=current_user, message="", len=0)


@auth.route('/logout')
@login_required
def logout():
    User.query.filter_by(id=current_user.get_id()).delete()
    db.session.commit()
    logout_user()
    return redirect(url_for('auth.login'))
