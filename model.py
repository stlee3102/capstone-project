"""Models for movie ratings app."""

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
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))

    user = db.relationship("User", backref="maps")

    def __repr__(self):
        return f'<Map map_id={self.map_id} start_pt={self.start_pt} end_pt={self.end_pt}>'



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