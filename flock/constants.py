# Stuff that doesn't change

session_duration = 1200
secret_key = "\x13`4\xf5\x90:(Qs\xa2\x0f\xd8\xbe\xee\x1b5Ae!\x9b\xd4\xe8\xf1\x94"
permissions = [
    'view_events',
    'edit_events',
    'view_people',
    'edit_people',
    'view_places',
    'edit_places',
    'edit_system_settings'
]

default_data = {
}

test_data = {
    'Person': [
        {"id": 1, "mail": "ian@m.ie", "name": "Ian Luddy", "invite": True, "active": True, "password": "pass",
         "company": 1, "role": 1, "role_name": "Manager", "role_theme": "success"},
        {"id": 2, "mail": "joe@m.ie", "name": "Joe Bloggs", "invite": True, "active": True, "password": "pass",
         "company": 1, "role": 2, "role_name": "Trainee", "role_theme": "danger"},
        {"id": 3, "mail": "john@m.ie", "name": "John Bloggs", "invite": True, "active": True, "password": "password",
         "company": 1, "role": 3, "role_name": "Connector", "role_theme": "warning", "token": None},
        {"id": 7, "mail": "ap@m.ie", "name": "Alan Partridge", "invite": True, "active": True, "password": "alan",
         "company": 1, "role": 3, "role_name": "Connector", "role_theme": "warning", "token": None},
        {"id": 107, "mail": "jaylin@m.ie", "name": "Jaylin Adcock", "invite": True, "active": False, "company": 1,
         "role": 2, "role_name": "Trainee", "role_theme": "danger", "token": "db891800-6030-475c-a925-0a079444bc28"},
        {"id": 108, "mail": "tracy@m.ie", "name": "Tracy Weekes", "invite": True, "active": False, "company": 1,
         "role": 5, "role_name": "Student", "role_theme": "primary", "token": "879d9147-ba5e-49e8-bacd-dc631fca337f"},
        {"id": 109, "mail": "blythe@m.ie", "name": "Blythe Poole", "invite": True, "active": False, "company": 1,
         "role": 2, "role_name": "Trainee", "role_theme": "danger", "token": "64fdc85d-8e8a-4777-9e90-10f4fff5e17b"},
        {"id": 110, "name": "Gyles Traviss", "invite": False, "active": False, "company": 1, "role": 2,
         "role_name": "Trainee", "role_theme": "danger"},
        {"id": 111, "mail": "davie@m.ie", "name": "Davie Sangster", "invite": False, "active": False, "company": 1,
         "role": 1, "role_name": "Manager", "role_theme": "success", "token": "ee82b1d5-9e4b-4e32-bd60-20a889ff782d"},
        {"id": 112, "mail": "jerrod@m.ie", "name": "Jerrod Hooper", "invite": True, "active": False, "company": 1,
         "role": 1, "role_name": "Manager", "role_theme": "success", "token": "21faa801-8d67-4fa4-8adb-5442eaf90104"},
        {"id": 113, "name": "Kyler Kendrick", "invite": False, "active": False, "company": 1, "role": 2,
         "role_name": "Trainee", "role_theme": "danger"},
        {"id": 114, "mail": "x@m.ie", "name": "Xavier Neville", "invite": True, "active": False, "company": 1,
         "role": 3, "role_name": "Connector", "role_theme": "warning", "token": "cfc5a323-9750-4909-9a4f-3e303996e200"},
        {"id": 115, "mail": "gage@m.ie", "name": "Gage Greene", "invite": True, "active": True, "company": 1, "role": 3,
         "role_name": "Connector", "role_theme": "warning", "token": None, "password": "pass"},
        {"id": 117, "name": "Erskine Abrams", "invite": False, "active": False, "company": 1, "role": 3,
         "role_name": "Connector", "role_theme": "warning"},
        {"id": 118, "mail": "norton@m.ie", "name": "Norton Garret", "invite": False, "active": False, "company": 1,
         "role": 5, "role_name": "Student", "role_theme": "primary"},
        {"id": 119, "name": "Dex Stevens", "invite": False, "active": False, "company": 1, "role": 5,
         "role_name": "Student", "role_theme": "primary"}
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
            'permissions': ['edit_events', 'edit_people', 'edit_places', 'edit_system_settings'],
            'company': 1,
            'theme': 'success'
        },
        {
            'id': 2,
            'name': 'Trainee',
            'permissions': ['edit_events', 'edit_people', 'edit_places'],
            'company': 1,
            'theme': 'danger'
        },
        {
            'id': 3,
            'name': 'Connector',
            'permissions': ['edit_events', 'edit_people', 'edit_places'],
            'company': 1,
            'theme': 'warning'
        },
        {
            'id': 4,
            'name': 'Independent',
            'permissions': ['edit_events', 'edit_people', 'edit_places'],
            'company': 1,
            'theme': 'info'
        },
        {
            'id': 5,
            'name': 'Student',
            'permissions': ['view_events', 'view_people', 'view_places'],
            'company': 1,
            'theme': 'primary'
        },
        {
            'id': 6,
            'name': 'External',
            'permissions': [],
            'company': 1,
            'theme': 'info'
        },
        {
            'id': 7,
            'name': 'System Administrator',
            'permissions': ['edit_events', 'edit_people', 'edit_places', 'edit_system_settings'],
            'company': 1,
            'theme': 'default'
        },
    ],
    'Place': [
        {
            'id': 1,
            'name': 'GEC',
            'address': 'Taylors Lane, Dublin 8',
            'mail': 'info@gec.ie',
            'phone': '01-234234234',
            'company': 1
        },
        {
            'id': 2,
            'name': 'Cake Venue',
            'address': 'Cake St, Dublin 12',
            'mail': 'info@cake.ie',
            'phone': '01-234234234',
            'company': 1
        },
        {
            'id': 3,
            'name': 'Square Tallaght',
            'address': 'Square, Tallaght',
            'mail': 'info@tallaght.ie',
            'phone': '01-234234234',
            'company': 1
        },
        {
            'id': 4,
            'name': 'Walk Office',
            'address': 'Walk, Walkinstown',
            'mail': 'info@walk.ie',
            'phone': '01-234234234',
            'company': 1
        },
        {
            'id': 5,
            'name': 'St. Catherines Gym',
            'address': 'Thomas St',
            'mail': 'info@gym.ie',
            'phone': '01-234234234',
            'company': 1
        },
    ],
    'Event': [
        {
            'id': 1,
            'title': 'Cake Class',
            'owner': 1,
            'people': [1,2,3],
            'place': 4,
            'company': 1
        },
        {
            'id': 2,
            'title': 'Reading Club',
            'owner': 1,
            'people': [1,2,3,7],
            'place': 1,
            'company': 1
        },
        {
            'id': 3,
            'title': 'Dancing',
            'owner': 1,
            'people': [1,2,112],
            'place': 3,
            'company': 1
        },
        {
            'id': 4,
            'title': 'Gym',
            'owner': 1,
            'people': [112,113,114],
            'place': 5,
            'company': 1
        },
        {
            'id': 5,
            'title': 'Dancing',
            'owner': 1,
            'people': [1,2,112],
            'place': 3,
            'company': 1
        },
        {
            'id': 6,
            'title': 'Gym',
            'owner': 1,
            'people': [112,113,114],
            'place': 5,
            'company': 1
        },
        {
            'id': 7,
            'title': 'Gym',
            'owner': 1,
            'people': [112,113,114],
            'place': 5,
            'company': 1
        },
        {
            'id': 8,
            'title': 'Dancing',
            'owner': 1,
            'people': [1,2,112],
            'place': 3,
            'company': 1
        },
        {
            'id': 9,
            'title': 'Gym',
            'owner': 1,
            'people': [112,113,114],
            'place': 5,
            'company': 1
        },
    ]
}