from flask import Blueprint, render_template, request, flash, redirect, url_for, g
from .login import is_valid_user
from .models import User
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('views.home'))
    if request.method == 'POST':
        uid = str(request.form.get('uid'))
        password = str(request.form.get('password'))

        if len(password) == 0 or len(uid) == 0:
            flash('Please provide both user ID and password', category='error')
        elif uid.isdigit() == False:
            flash('User ID should be numeric', category='error')
        elif not is_valid_user(uid, password):
            flash('Invalid user ID/password, or SAP is unreachable', category='error')
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
            flash('Successfully logged in!', category='success')
            print(User.query.get(password))
            return redirect(url_for('views.home'))

    return render_template('login.html', user=current_user)

@auth.route('/logout')
@login_required
def logout():
    User.query.filter_by(id=current_user.get_id()).delete()
    db.session.commit()
    logout_user()
    return redirect(url_for('auth.login'))
