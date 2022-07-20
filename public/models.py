from app import db


class PremiumUserMapping(db.Model):
    """model for premium user mapping who buys subscription"""

    __tablename__ = "premium_user_mapping"
    premium_user_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    purchase_date = db.Column(db.DateTime)
