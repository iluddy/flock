from flock.app import db_wrapper as db
from flock.services.notification import notify

def add(new_place):
    db.place_add(new_place)
    notify(u'{} added a new Place - <b>%s</b>' % new_place['name'], action='add', target='place')

def delete(place_id):
    place_name = db.place_get(place_id=place_id).name
    db.place_delete(place_id)
    notify(u'{} deleted a Place - <b>%s</b>' % place_name, action='delete', target='place')

def get(company_id, search=None, sort_by=None, sort_dir=None, limit=None, offset=None):
    return db.place_get(company_id, search=search, sort_by=sort_by, sort_dir=sort_dir, limit=limit, offset=offset)