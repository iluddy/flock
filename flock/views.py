from flask import request, redirect, url_for, render_template, session
from flock import app
from flock import person_service, place_service, account_service, event_service, role_service
from flock import db_wrapper
from flock.utils import json_response, auth

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

#### User Account/Session ####

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/activate/<token>')
def activate_form(token):
    person = db_wrapper.person_get(None, token=token)
    # TODO - deal with not finding user
    # TODO - list terms and conditions on activate and register pages
    # TODO - validate password on frontend
    return render_template('activate.html', token=token, name=person.name, email=person.mail)

@app.route('/activate', methods=['POST'])
def activate_account():
    token = request.form.get("token")
    name = request.form.get("name")
    password = request.form.get("password")
    mail = request.form.get("email")

    db_wrapper.activate_user(token, name, password)
    session['user_id'], session['user_name'], session['company_id'], session['company_name'] = \
        db_wrapper.authenticate_user(mail, password)

    return 'Account Activated :)', 200

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
    db_wrapper.register_user(
        request.form.get("name"),
        request.form.get("mail"),
        request.form.get("password"),
        request.form.get("company"),
    )
    return login_user()

@app.route('/login_user', methods=['POST'])
def login_user():
    session['user_id'], session['user_name'], session['company_id'], session['company_name'] = \
        db_wrapper.authenticate_user(request.form.get('mail'), request.form.get('password'))
    return 'Logged in :)', 200

@app.route('/reset_user', methods=['POST'])
def reset_user():
    account_service.reset(request.form.get("mail"))
    return 'Password reset. You should receive an email shortly :)', 200

#### People ####

@app.route('/people', methods=['DELETE'])
@auth
def people_delete():
    person_service.delete(request.form.get("id"))
    return '{} has been deleted'.format(request.form.get("name")), 200

@app.route('/people', methods=['GET', 'POST'])
@auth
def people():
    search = request.form.get("search", None)
    sort_by = request.form.get("sort_by", None)
    sort_dir = request.form.get("sort_dir", None)
    limit = request.form.get("limit", 10)
    offset = request.form.get("offset", 0)
    data, count = person_service.get(session['company_id'], search=search, sort_by=sort_by, sort_dir=sort_dir, limit=limit, offset=offset)
    return json_response({'data': data, 'count': count})

@app.route('/people', methods=['PUT'])
@auth
def people_add():
    invite = request.form.get("invite", None)
    new_person = {
        'name': request.form.get("name", None),
        'mail': request.form.get("mail", None),
        'role': request.form.get("type", None),
        'invite': True if invite else False,
        'company': session['company_id']
    }
    person_service.add(new_person, session['user_id'], session['company_id'])
    return '{} has been added'.format(new_person['name']), 200

@app.route('/people/invite', methods=['POST'])
@auth
def people_invite():
    mail = request.form.get("mail")
    person_service.invite(mail, session['user_id'], session['company_id'])
    return 'Invitation has been sent to {}'.format(mail), 200

#### Places ####

@app.route('/places', methods=['DELETE'])
@auth
def places_delete():
    place_service.delete(request.form.get("id"))
    return '{} has been deleted'.format(request.form.get("name")), 200

@app.route('/places', methods=['GET', 'POST'])
@auth
def places():
    search = request.form.get("search", None)
    sort_by = request.form.get("sort_by", None)
    sort_dir = request.form.get("sort_dir", None)
    limit = request.form.get("limit", 10)
    offset = request.form.get("offset", 0)
    data, count = place_service.get(session['company_id'], search=search, sort_by=sort_by, sort_dir=sort_dir, limit=limit, offset=offset)
    return json_response({'data': data, 'count': count})

@app.route('/places', methods=['PUT'])
@auth
def places_add():
    new_place = {
        'name': request.form.get("name", None),
        'mail': request.form.get("email", None),
        'phone': request.form.get("phone", None),
        'address': request.form.get("address", None),
        'company': session['company_id']
    }
    place_service.add(new_place)
    return '{} has been added'.format(new_place['name']), 200

#### Events ####

@app.route('/events')
@auth
def events():
    return json_response(event_service.get(session['company_id']))

#### Roles ####

@app.route('/roles')
@auth
def roles():
    return json_response(role_service.get(company_id=session['company_id']))

@app.route('/roles', methods=['PUT'])
@auth
def roles_update():
    role = {
        "theme": request.form.get("theme"),
        "name": request.form.get("name"),
        "role_type": int(request.form.get("type"))
    }
    if request.form.get('id'):
        role['id'] = int(request.form.get('id'))
        role_service.update(role, session['company_id'])

    role_service.add(role, session['company_id'])

    return 'People Types Updated', 200

@app.route('/roles', methods=['DELETE'])
@auth
def roles_delete():
    # TODO - validate deletion
    role_service.delete(request.form.get("id"))
    return 'People Types Updated', 200

#### Role Type ####

@app.route('/role_types')
@auth
def role_types():
    # TODO - remove db-wrapper
    return json_response(db_wrapper.get_role_types())
