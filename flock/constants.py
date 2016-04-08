# Stuff that doesn't change
# -*- coding: utf-8 -*-

SESSION_DURATION = 1200
SECRET_KEY = "\x13`4\xf5\x90:(Qs\xa2\x0f\xd8\xbe\xee\x1b5Ae!\x9b\xd4\xe8\xf1\x94"
PERMISSIONS = [
    'view_events',
    'edit_events',
    'view_people',
    'edit_people',
    'view_places',
    'edit_places',
    'edit_system_settings'
]

PAGE_SIZE = 15

DEFAULT_DATA = {
}

TEST_DATA = {
    'Role': [
        {
            'id': -1,
            'name': 'Manager',
            'permissions': ['edit_events', 'edit_people', 'edit_places', 'edit_system_settings'],
            'company': -1,
            'theme': 'success'
        },
        {
            'id': -2,
            'name': 'Trainee',
            'permissions': ['edit_events', 'edit_people', 'edit_places'],
            'company': -1,
            'theme': 'danger'
        },
        {
            'id': -3,
            'name': 'Connector',
            'permissions': ['edit_events', 'edit_people', 'edit_places'],
            'company': -1,
            'theme': 'warning'
        },
        {
            'id': -4,
            'name': 'Independent',
            'permissions': ['edit_events', 'edit_people', 'edit_places'],
            'company': -1,
            'theme': 'info'
        },
        {
            'id': -5,
            'name': 'Student',
            'permissions': ['view_events', 'view_people', 'view_places'],
            'company': -1,
            'theme': 'primary'
        },
        {
            'id': -6,
            'name': 'External',
            'permissions': [],
            'company': -1,
            'theme': 'info'
        }
    ],
    'Person': [
        {
            "id": -1,
            "mail": "ian@tryflock.com",
            "name": "Ian Luddy",
            "invite": True,
            "active": True,
            "password": "pbkdf2:sha1:1000$Ejjo3uqM$04d48dc71ce6460f6454f403ef6e331ce7acfad3",
            "company": -1
        },
        {
            "id": -2,
            "mail": "dani@tryflock.com",
            "name": "Dani Brown",
            "invite": True,
            "active": True,
            "password": "pbkdf2:sha1:1000$Ejjo3uqM$04d48dc71ce6460f6454f403ef6e331ce7acfad3",
            "company": -1,
            "role": -1,
            "role_name": "Manager",
            "role_theme": "success"
        },
        {
            "id": -3,
            "mail": "kacper@tryflock.com",
            "name": "Kacper Oppegård",
            "invite": True,
            "active": True,
            "password": "pbkdf2:sha1:1000$Ejjo3uqM$04d48dc71ce6460f6454f403ef6e331ce7acfad3",
            "company": -1,
            "role": -1,
            "role_name": "Manager",
            "role_theme": "success"
        },
        {
            "id": -4,
            "mail": "牛禹凡@tryflock.com",
            "name": "牛禹凡",
            "invite": True,
            "active": False,
            "password": "pbkdf2:sha1:1000$Ejjo3uqM$04d48dc71ce6460f6454f403ef6e331ce7acfad3",
            "company": -1,
            "role": -3,
            "role_name": "Connector",
            "role_theme": "warning"
        },
        {
            "id": -5,
            "mail": "jürgen@tryflock.com",
            "name": "Jürgen Wexler",
            "invite": True,
            "active": False,
            "password": "pbkdf2:sha1:1000$Ejjo3uqM$04d48dc71ce6460f6454f403ef6e331ce7acfad3",
            "company": -1,
            "role": -3,
            "role_name": "Connector",
            "role_theme": "warning"
        },
        {
            "id": -6,
            "mail": "erskine@tryflock.com",
            "name": "Erskine Abrams",
            "invite": True,
            "active": False,
            "password": "pbkdf2:sha1:1000$Ejjo3uqM$04d48dc71ce6460f6454f403ef6e331ce7acfad3",
            "company": -1,
            "role": -3,
            "role_name": "Connector",
            "role_theme": "warning"
        },
        {
            "id": -7,
            "mail": "joe@tryflock.com",
            "name": "Joe Bloggs",
            "invite": True,
            "active": True,
            "password": "pbkdf2:sha1:1000$Ejjo3uqM$04d48dc71ce6460f6454f403ef6e331ce7acfad3",
            "company": -1,
            "role": -2,
            "role_name": "Trainee",
            "role_theme": "danger"
        },
        {
            "id": -8,
            "mail": "jim@tryflock.com",
            "name": "Jim Bloggs",
            "invite": True,
            "active": True,
            "password": "pbkdf2:sha1:1000$Ejjo3uqM$04d48dc71ce6460f6454f403ef6e331ce7acfad3",
            "company": -1,
            "role": -2,
            "role_name": "Trainee",
            "role_theme": "danger"
        },
        {
            "id": -9,
            "mail": "jaylin@tryflock.com",
            "name": "Jaylin Adcock",
            "invite": True,
            "active": True,
            "password": "pbkdf2:sha1:1000$Ejjo3uqM$04d48dc71ce6460f6454f403ef6e331ce7acfad3",
            "company": -1,
            "role": -2,
            "role_name": "Trainee",
            "role_theme": "danger"
        },
        {
            "id": -10,
            "mail": "gyles@tryflock.com",
            "name": "Gyles Traviss",
            "invite": True,
            "active": True,
            "password": "pbkdf2:sha1:1000$Ejjo3uqM$04d48dc71ce6460f6454f403ef6e331ce7acfad3",
            "company": -1,
            "role": -2,
            "role_name": "Trainee",
            "role_theme": "danger"
        }
    ],
    'Company': [
        {
            'id': -1,
            'name': 'IanCO',
            'owner': -1
        }
    ],
    'Place': [
        {
            'id': -1,
            'name': 'GEC',
            'address': 'Taylors Lane, Dublin 8',
            'mail': 'info@gec.ie',
            'phone': '01-234234234',
            'company': -1
        },
        {
            'id': -2,
            'name': 'Mannings Bakery',
            'address': '12 Thomas St, Dublin 8',
            'mail': 'info@mannings.ie',
            'phone': '01-234234234',
            'company': -1
        },
        {
            'id': -3,
            'name': 'Square Tallaght',
            'address': 'Square, Tallaght',
            'mail': 'info@tallaght.ie',
            'phone': '01-234234234',
            'company': -1
        },
        {
            'id': -4,
            'name': 'Walk Office',
            'address': 'Walk, Walkinstown',
            'mail': 'info@walk.ie',
            'phone': '01-234234234',
            'company': -1
        },
        {
            'id': -5,
            'name': 'St. Catherines Gym',
            'address': 'Thomas St',
            'mail': 'info@gym.ie',
            'phone': '01-234234234',
            'company': -1
        },
    ]
}