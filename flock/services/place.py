from flock.app import db_wrapper as db

def add(new_place):
    db.place_add(new_place)

def delete(place_id):
    db.place_delete(place_id)

def get(company_id, search=None, sort_by=None, sort_dir=None, limit=None, offset=None):
    return db.place_get(company_id, search=search, sort_by=sort_by, sort_dir=sort_dir, limit=limit, offset=offset)