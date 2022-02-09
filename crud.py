"""CRUD operations."""

from model import db, User, Map, Store, PackingList, Categories, connect_to_db

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

def delete_user(user_id):
    """Delete user"""
    selected_user = User.query.filter(User.user_id==user_id).first()
    user_maps = Map.query.filter(Map.user == selected_user).all()
    user_packing_list = PackingList.query.filter(PackingList.user == selected_user).all()

    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    print(selected_user)
    print(user_maps)
    print(user_packing_list)
    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!")

    
    db.session.delete(selected_user)
    for map in user_maps:
        db.session.delete(map)
    for packing_list in user_packing_list:
        db.session.delete(packing_list)
    db.session.commit()

def create_map(start_pt, end_pt, mode, user_id):
    """Create and return a new saved map."""

    map = Map(start_pt=start_pt, end_pt=end_pt, mode=mode, user_id=user_id)

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

def return_all_stores():
    """Return all stores"""
    return Store.query.all()

def add_item(user_id, item_name, category_name, quantity, status):
    """Create and return a new packing list row for a new item."""
    category = db.session.query(Categories).filter_by(category_name=category_name).first()
    if not category:
       category = Categories(category_name=category_name)
       db.session.add(category)
       db.session.commit()

    plist = PackingList(user_id=user_id, item_name=item_name, category_id=category.category_id, quantity=quantity, status=status)

    db.session.add(plist)
    db.session.commit()

    return plist

def add_category(category_name):
    """Create a new category."""

    category = Categories(category_name=category_name)

    db.session.add(category)
    db.session.commit()

    return category

def get_packing_list_by_user_id(user_id):
    """Return packing list by user id"""

    return PackingList.query.filter(PackingList.user_id == user_id).order_by(PackingList.category_id, PackingList.item_id).all()

def get_categories():
    """Return category list"""
    return Categories.query.all()

def return_all_packing_lists():
    """Return all packing lists"""
    return PackingList.query.order_by(PackingList.category_id, PackingList.item_id).all()

def delete_item(item_id):
    """Delete item from packing list"""
    item = PackingList.query.filter(PackingList.item_id==item_id).first()
    db.session.delete(item)
    db.session.commit()

def delete_category(category_name):
    """Delete category for packing list. Any items with the deleted category will be reassigned to Miscellaneous"""

    deleted_category = Categories.query.filter(Categories.category_name==category_name).first()
    deleted_category_id = deleted_category.category_id

    misc_category = Categories.query.filter(Categories.category_name=="Miscellaneous").first()

    items = PackingList.query.filter(PackingList.category_id==deleted_category_id).all()

    for item in items:
        item.category = misc_category

    db.session.delete(deleted_category)
    db.session.commit()


def change_item_status(item_id, status):
    """Change status of item in Packing List"""

    item = PackingList.query.filter(PackingList.item_id==item_id).first()

    if item.status == False:
        item.status = True
    else:
        item.status = False
    db.session.add(item)
    db.session.commit()

def change_item_qty(item_id, qty):
    """Change qty of item in Packing List"""

    item = PackingList.query.filter(PackingList.item_id==item_id).first()

    item.quantity = qty
    db.session.add(item)
    db.session.commit()


if __name__ == '__main__':
    from server import app
    connect_to_db(app)