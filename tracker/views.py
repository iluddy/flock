from flask import request, redirect, url_for, render_template, session
from tracker import app
from tracker import task_manager
from tracker import db_wrapper
from tracker.utils import json_response, auth


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

#### People ####

@app.route('/people', methods=['GET', 'POST'])
@auth
def people():
    roles = request.form.get("roles", None)
    return json_response(db_wrapper.get_people(roles=roles))

@app.route('/people/add', methods=['POST'])
@auth
def people_add():
    invite_person = request.form.get("invite", None)
    new_person = {
        'name': request.form.get("name", None),
        'mail': request.form.get("mail", None),
        'role': request.form.get("type", None),
        'invite': False if invite_person else None,
        'company': session['company_id']
    }
    db_wrapper.add_person(new_person)

    if invite_person:
        task_manager.push({
            'action': 'invite',
            'email': request.form.get("mail", None)
         })

    return 'New Person Added: %s' % new_person['name'], 200

@app.route('/people/reinvite', methods=['POST'])
@auth
def people_reinvite():
    task_manager.push({
        'action': 'invite',
        'email': request.form.get("mail", None)
    })

    return 'Invitation will be sent', 200

#### Roles ####

@app.route('/roles')
@auth
def roles():
    return json_response(db_wrapper.get_roles())

@app.route('/role_types')
@auth
def role_types():
    return json_response(db_wrapper.get_role_types())

@app.route('/roles/update', methods=['POST'])
@auth
def roles_update():
    updated_role = {
        "theme": request.form.get("theme"),
        "name": request.form.get("name"),
        "role_type": int(request.form.get("type"))
    }
    if request.form.get('id'):
        updated_role['id'] = int(request.form.get('id'))
    db_wrapper.update_role(updated_role)
    return 'People Types Updated', 200

@app.route('/roles/delete', methods=['POST'])
@auth
def roles_delete():
    # TODO - validate deletion
    db_wrapper.delete_role(request.form.get("id"))
    return 'People Types Updated', 200
