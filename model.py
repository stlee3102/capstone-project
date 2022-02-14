from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    """A user."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    fname = db.Column(db.String)
    lname = db.Column(db.String)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.LargeBinary)

    # maps = a list of Map objects
    # packinglists = a list of Packing List objects
    # categories = a list of Category objects

    def __repr__(self):
        return f'<User user_id={self.user_id} email={self.email}>'

class Map(db.Model):
    """A map."""

    __tablename__ = "maps"

    map_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    start_pt = db.Column(db.String)
    end_pt = db.Column(db.String)
    mode = db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))

    user = db.relationship("User", backref="maps")

    def __repr__(self):
        return f'<Map map_id={self.map_id} start_pt={self.start_pt} end_pt={self.end_pt}>'

class Store(db.Model):
    """Store information."""

    __tablename__ = "stores"

    store_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    name = db.Column(db.String)
    address = db.Column(db.String)
    city = db.Column(db.String)
    state = db.Column(db.String)
    zip = db.Column(db.String)
    phone = db.Column(db.String)
    hours = db.Column(db.String)
    lat = db.Column(db.Float)
    long = db.Column(db.Float)


    def __repr__(self):
        return f'<Store store_id={self.store_id} name={self.name} lat={self.lat} long={self.long}>'

class PackingList(db.Model):
    """A Packing List."""

    __tablename__ = "packinglists"
    item_id = db.Column(db.Integer,
                    autoincrement=True,
                    primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))
    item_name = db.Column(db.String)
    category_id = db.Column(db.Integer, db.ForeignKey("categories.category_id"))
    quantity = db.Column(db.Integer)
    status = db.Column(db.Boolean)

    user = db.relationship("User", backref="packinglists")
    category = db.relationship("Categories", backref="packinglists")

    def __repr__(self):
        return f'<PackingList item_id={self.item_id} category_name={self.category_id} item={self.item_name} quantity={self.quantity} status={self.status}>'


class Categories(db.Model):
    """Categories of items for Packing List."""

    __tablename__ = "categories"

    category_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    category_name = db.Column(db.String, unique=True, index=True)
   
    def __repr__(self):
        return f'<Categories category_id={self.category_id} category_name={self.category_name}>'

def example_data():
    """Example data for integration testing"""
    User.query.delete()
    Map.query.delete()
    Store.query.delete()
    PackingList.query.delete()
    Categories.query.delete()

    #add users
    user1 = User(fname="Admin", lname="Test", email="admin@test.com", password=b"\x30\xdc\x7d\x12\xf7\xec\x08\xf6\x0c\x05\x38\xbb\x3a\x28\x50\x02\xd5\x26\xcd\x9d\x46\x95\x35\x2b\x08\x18\x80\x36\x5c\x51\x79\x61\xa8\xa0\xe7\x21\xb3\x56\x92\x34\xd3\xa9\x0b\xc6\x0f\x71\xba\x76\x8b\x49\x11\x22\x20\x85\xee\x03\x0f\xbf\x52\xdf\x03\x31\x0a\x03\x94\xd7\x31\x35\xc5\xd7\x9f\x29\x6a\x40\x16\x89\xad\x29\x92\x1b\xf7\x74\x56\x53\x12\x9a\x56\x03\x99\x35\x10\xce\x06\xaf\xc5\x08\xc7\xab\x96\x5e\xcb\x37\xe7\xd7\xa8\x90\x36\x41\x01\xd8\x39\x1f\xc0\x0f\x38\x3e\x22\x31\x97\x4a\xd8\xc4\xcb\x82\xa9\x83\x35\xd1\x82\xf8\x74\xe4\x2f\x74\x4c\xaf\x1f\xd1\x83\xec\xdc\xee\x4e\xce\x78\x92\x91\x74\x21\x5e\xfa\xc5\x5f\xb9\x1c\xd5\x40\x20\xa4\xf7")
    user2 = User(fname="Jane", lname="Smith", email="jane@test.com", password=b"test")
    
    db.session.add(user1)
    db.session.add(user2)
    db.session.commit()

    #add maps
    map1 = Map(
        start_pt="585 Franklin St, Mountain View, CA 94041",
        end_pt="160 N Main St, Milpitas, CA 95035",
        mode = "Driving",
        user_id=1
    )

    map2 = Map(
        start_pt="1276 Harriet St, Palo Alto, CA 94301",
        end_pt="350 W 6th St, Gilroy, CA 95020", 
        mode = "Driving", 
        user_id=2
    )

    db.session.add(map1)
    db.session.add(map2)
    db.session.commit()

    #add stores
    store_info1 = Store(
        name="Mountain View Store",
        address="600 Showers Dr",
        city="Mountain View",
        state="CA",
        zip="94040",
        phone="650-917-0796",
        hours="monday - friday : 07:00-22:00, saturday : 07:00-22:00, sunday : 07:00-22:00",
        lat=37.400846,
        long=-122.109748
    )

    store_info2 = Store(
        name="Milpitas Supercenter",
        address="301 Ranch Dr",
        city="Milpitas",
        state="CA",
        zip="95035",
        phone="408-934-0304",
        hours="monday - friday : 06:00-24:00, saturday : 06:00-24:00, sunday : 06:00-24:00",
        lat=37.431416,
        long=-121.921182
    )
    
    db.session.add(store_info1)
    db.session.add(store_info2)
    db.session.commit()

    #add categories
    cat1 = Categories(category_name="Clothes")
    cat2 = Categories(category_name="Medical")
    db.session.add(cat1)
    db.session.add(cat2)
    db.session.commit()

    #add packing list items for users
    item1 = PackingList(user_id=1, item_name="Shirt", category_id=1, quantity=2, status=False)
    item2 = PackingList(user_id=1, item_name="Pants", category_id=1, quantity=3, status=True)
    item3 = PackingList(user_id=1, item_name="Vitamins", category_id=2, quantity=1, status=False)
    item4 = PackingList(user_id=2, item_name="Socks", category_id=1, quantity=4, status=False)
    item5 = PackingList(user_id=2, item_name="Dress", category_id=1, quantity=3, status=True)
    item6 = PackingList(user_id=2, item_name="Medicine Pills", category_id=2, quantity=10, status=False)

    db.session.add(item1)
    db.session.add(item2)
    db.session.add(item3)
    db.session.add(item4)
    db.session.add(item5)
    db.session.add(item6)
    db.session.commit()

def connect_to_db(flask_app, db_uri="postgresql:///mapdb", echo=True):
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    flask_app.config["SQLALCHEMY_ECHO"] = echo
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.app = flask_app
    db.init_app(flask_app)

    print("Connected to the db!")


if __name__ == "__main__":
    from server import app

    #echo false prevents SQLAlchemy from printing every query
    connect_to_db(app, echo=False)