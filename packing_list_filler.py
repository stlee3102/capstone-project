"""Automatically fill in Packing List and Category Data

    Must Be Run AFTER Users Have Been Filled In
    Run user_map_db_filler.py first

"""

from model import db, PackingList, Categories, connect_to_db

from server import app
connect_to_db(app)

#Categories
cat1 = Categories(category_name="Clothes")
db.session.add(cat1)
db.session.commit()

cat2 = Categories(category_name="Medical")
db.session.add(cat2)
db.session.commit()

cat3 = Categories(category_name="Camping Equipment")
db.session.add(cat3)
db.session.commit()

cat4 = Categories(category_name="Entertainment")
db.session.add(cat4)
db.session.commit()

cat5 = Categories(category_name="Accessories")
db.session.add(cat5)
db.session.commit()

cat6 = Categories(category_name="Toiletries")
db.session.add(cat6)
db.session.commit()


#Items for Admin
item1 = PackingList(user_id=1, item_name="Shirt", category_id=1, quantity=2, status=False)
db.session.add(item1)
db.session.commit()

item2 = PackingList(user_id=1, item_name="Pants", category_id=1, quantity=3, status=True)
db.session.add(item2)
db.session.commit()

item3 = PackingList(user_id=1, item_name="Vitamins", category_id=2, quantity=1, status=False)
db.session.add(item3)
db.session.commit()

#Items for Test User Jane
item4 = PackingList(user_id=2, item_name="Socks", category_id=1, quantity=4, status=False)
db.session.add(item4)
db.session.commit()

item5 = PackingList(user_id=2, item_name="Dress", category_id=1, quantity=3, status=True)
db.session.add(item5)
db.session.commit()

item6 = PackingList(user_id=2, item_name="Medicine Pills", category_id=2, quantity=10, status=False)
db.session.add(item6)
db.session.commit()
