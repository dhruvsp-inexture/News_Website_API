from flask import current_app
from app import db
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer


class UserType(db.Model):
    """model for storing different types of user along with their ids"""

    __tablename__ = "user_type"
    user_type_id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(20), unique=True, nullable=False)
    # type_of_user = db.relationship('User', backref='usertype', lazy=True)
    # journalist_news = db.relationship('JournalistNewsMapping', backref='journalistnews', lazy=True)

    def save_to_db(self) -> "UserType":
        db.session.add(self)
        db.session.commit()
        return self


class User(db.Model):
    """model for storing user information and user id"""

    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    has_premium = db.Column(db.Boolean, default=False, nullable=False)
    user_type_id = db.Column(db.Integer, db.ForeignKey('user_type.user_type_id'))

    def get_reset_token(self, expires_sec=1800):
        """function to get the reset token which will expire in 30 minutes

        Parameters
        ----------
        expires_sec: int
            time to expire the token in seconds

        Returns
        -------
        string
            contains the token by converting json to string
        """

        serializer = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return serializer.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        """function for verifying the reset token

        Parameters
        ----------
        token: str
            token which is generated while requesting reset password is loaded here
        Returns
        -------
        object
            contains the user object from given user_id
        """

        serializer = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = serializer.loads(token)['user_id']
        except (KeyError, Exception):
            return None
        return User.query.get(user_id)

    def save_to_db(self) -> "User":
        db.session.add(self)
        db.session.commit()
        return self
