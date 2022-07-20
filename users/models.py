from app import db


class UserType(db.Model):
    """model for storing different types of user along with their ids"""

    __tablename__ = "user_type"
    user_type_id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(20), unique=True, nullable=False)
    # type_of_user = db.relationship('User', backref='usertype', lazy=True)
    # journalist_news = db.relationship('JournalistNewsMapping', backref='journalistnews', lazy=True)


class User(db.Model):
    """model for storing user information and user id"""

    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    has_premium = db.Column(db.Boolean, default=False, nullable=False)
    user_type_id = db.Column(db.Integer, db.ForeignKey('user_type.user_type_id'))

    def save_to_db(self) -> "User":
        db.session.add(self)
        db.session.commit()
        return self
