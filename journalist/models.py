import datetime
from sqlalchemy import PrimaryKeyConstraint
from app import db


class NewsCategory(db.Model):
    """model for different categories of news"""

    __tablename__ = "news_category"
    category_id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(30), unique=True, nullable=False)
    # category_type = db.relationship('News', backref='categorytype', lazy=True)

    def save_to_db(self) -> "NewsCategory":
        db.session.add(self)
        db.session.commit()
        return self


class News(db.Model):
    """model for news and its information"""

    __tablename__ = "news"
    news_id = db.Column(db.Integer, primary_key=True)
    news_heading = db.Column(db.String, nullable=False)
    news_info = db.Column(db.String, nullable=False)
    news_date = db.Column(db.DateTime, default=datetime.datetime.today())
    is_approved = db.Column(db.Boolean)
    checked = db.Column(db.Boolean, default=False)
    image = db.Column(db.String, default=None)
    news_category_id = db.Column(db.Integer, db.ForeignKey('news_category.category_id'))
    # news_journalist = db.relationship('JournalistNewsMapping', backref='newsjournalist', lazy=True)

    def save_to_db(self) -> "News":
        db.session.add(self)
        db.session.commit()
        return self


class JournalistNewsMapping(db.Model):
    """model for mapping journalist(user) id and news id"""

    __tablename__ = "journalist_news_mapping"
    __table_args__ = (
        PrimaryKeyConstraint('journalist_id', 'news_id'),
    )
    journalist_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    news_id = db.Column(db.Integer, db.ForeignKey('news.news_id'), nullable=False)

    def save_to_db(self) -> "JournalistNewsMapping":
        db.session.add(self)
        db.session.commit()
        return self

