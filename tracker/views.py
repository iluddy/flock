from tracker import app
from tracker import db_wrapper
from tracker.constants import session_duration
import datetime
from functools import wraps
from flask import request, redirect, url_for, render_template, session
from time import sleep

def auth(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('user_id'):
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function


@app.route('/')
@auth
def root():
    return render_template(
        'index.html',
        user_name=session['user_name'],
        user_id=session['user_id'],
        company_id=session['company_id'],
        company_name=session['company_name'],
    )

@app.route('/templates')
@auth
def templates():
    print 123
    return app.send_static_file('hb_templates/templates.html')

#### User Session ####

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/forgot_password')
def forgot_password():
    return render_template('forgot_password.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('company_id', None)
    session.pop('company_name', None)
    session.pop('user_name', None)
    return redirect(url_for('login'))

@app.route('/registration')
def registration():
    return render_template('register.html')

@app.route('/register', methods=['POST'])
def register():
    success, message = db_wrapper.register_user(
        request.form.get("name"),
        request.form.get("mail"),
        request.form.get("password"),
        request.form.get("company"),
    )
    if not success:
        return message, 422
    return login_user()

@app.route('/login_user', methods=['POST'])
def login_user():
    success, message = db_wrapper.authenticate_user(request.form.get('mail'), request.form.get('password'))
    if success:
        return message, 200
    return message, 401

@app.route('/reset_user', methods=['POST'])
def reset_user():
    success, message = db_wrapper.reset_user(request.form.get('mail'))
    if success:
        return message, 200
    return message, 401

#### User ####

#### Company ####