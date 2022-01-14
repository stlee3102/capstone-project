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
    password = db.Column(db.String)

    # maps = a list of Map objects

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



def connect_to_db(flask_app, db_uri="postgresql:///mapdb", echo=True):
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    flask_app.config["SQLALCHEMY_ECHO"] = echo
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.app = flask_app
    db.init_app(flask_app)

    print("Connected to the db!")


if __name__ == "__main__":
    from server import app

    connect_to_db(app)