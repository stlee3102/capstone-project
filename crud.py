"""CRUD operations."""

from model import db, User, Map, Store, connect_to_db

def create_user(fname, lname, email, password):
    """Create and return a new user."""

    user = User(fname=fname, lname=lname, email=email, password=password)

    db.session.add(user)
    db.session.commit()

    return user

def return_all_users():
    """Return all users"""
    return User.query.all()

def get_user_by_id(user_id):
    """Return user from user id"""

    return User.query.get(user_id)

def get_user_by_email(email):
    """Return user from email"""

    return User.query.filter(User.email == email).first()

def create_map(start_pt, end_pt, user_id):
    """Create and return a new saved map."""

    map = Map(start_pt=start_pt, end_pt=end_pt, user_id=user_id)

    db.session.add(map)
    db.session.commit()

    return map

def get_maps_by_user_id(user_id):
    """Return map by user id"""

    return Map.query.filter(Map.user_id == user_id).all()


def return_all_maps():
    """Return all maps"""
    return Map.query.all()

def delete_map(map_id):
    """Delete a map"""

    map = Map.query.filter(Map.map_id==map_id).first()

    db.session.delete(map)
    db.session.commit()




if __name__ == '__main__':
    from server import app
    connect_to_db(app)