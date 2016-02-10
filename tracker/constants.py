# Stuff that doesn't change

session_duration = 1200
secret_key = "\x13`4\xf5\x90:(Qs\xa2\x0f\xd8\xbe\xee\x1b5Ae!\x9b\xd4\xe8\xf1\x94"

default_data = {
    'RoleType': [
        {
            'id': 1,
            'name': 'Admin User',
            'description': 'Administrate stuff',
        },
        {
            'id': 2,
            'name': 'Normal User',
            'description': 'Normal stuff'
        },
        {
            'id': 3,
            'name': 'Basic User',
            'description': 'Read Only'
        },
    ]
}

test_data = {
    'Person': [
        {
            'id': 1,
            'name': 'Ian Luddy',
            'mail': 'ian@m.ie',
            'password': 'pass',
            'company': 1,
            'role': 1
        },
        {
            'id': 2,
            'name': 'Joe Bloggs',
            'mail': 'joe@m.ie',
            'password': 'pass',
            'company': 1,
            'role': 2
        },
    ],
    'Company': [
        {
            'id': 1,
            'name': 'IanCO'
        }
    ],
    'Role': [
        {
            'id': 1,
            'name': 'Manager',
            'role_type': 1,
            'company': 1,
            'theme': 'success'
        },
        {
            'id': 2,
            'name': 'Trainee',
            'role_type': 2,
            'company': 1,
            'theme': 'danger'
        }

    ]
}