import os
from datetime import datetime

from flask import Flask

from app import bcrypt
import pytest
from flask_migrate import Migrate
from dotenv import load_dotenv
from users.models import User, UserType
from journalist.models import NewsCategory, News, JournalistNewsMapping

load_dotenv()


@pytest.fixture(scope="session")
def app():
    from app import create_app
    # app = Flask(__name__)
    # app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("TEST_DATABASE_URI")
    # app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    # app.config['PROPAGATE_EXCEPTIONS'] = True
    # app.config['TESTING'] = True
    return create_app()


@pytest.fixture(scope="function", autouse=True)
def db(app):
    from app import db
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("TEST_DATABASE_URI")
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['PROPAGATE_EXCEPTIONS'] = True
    app.config['TESTING'] = True
    db.init_app(app)
    print("-------Creating Tables------")
    with app.app_context():
        db.create_all(app=app)
    Migrate(app, db)
    db.init_app(app)
    yield db
    print("-------Dropping Tables------")
    with app.app_context():
        db.drop_all(app=app)


@pytest.fixture(scope="session")
def client(app):
    return app.test_client()


@pytest.fixture(scope="function")
def user(app, db):
    with app.app_context():
        user_type_object = UserType(user_type_id=1, type="admin")
        user_type_object.save_to_db()

        user_type_object = UserType(user_type_id=2, type="journalist")
        user_type_object.save_to_db()

        user_type_object = UserType(user_type_id=3, type="user")
        user_type_object.save_to_db()

        category_type_object = NewsCategory(category="General")
        category_type_object.save_to_db()

        category_type_object = NewsCategory(category="Entertainment")
        category_type_object.save_to_db()

        password = bcrypt.generate_password_hash("abc")
        user_object = User(name="Admin", email="admin@gmail.com", password=password,
                           user_type_id=1)
        user_object.save_to_db()

        user_object = User(name="Journalist", email="journalist@gmail.com", password=password,
                           user_type_id=2)
        user_object.save_to_db()

        news_object = News(news_heading="heading 1", news_info="info 1", news_date=datetime.now(), news_category_id=1)
        news_object.save_to_db()

        journalist_news_object = JournalistNewsMapping(journalist_id=user_object.id, news_id=news_object.news_id)
        journalist_news_object.save_to_db()

        news_object = News(news_heading="heading 2", news_info="info 2", news_date=datetime.now(), news_category_id=1,
                           is_approved=True, checked=True)
        news_object.save_to_db()

        journalist_news_object = JournalistNewsMapping(journalist_id=user_object.id, news_id=news_object.news_id)
        journalist_news_object.save_to_db()

        news_object = News(news_heading="heading 3", news_info="info 3", news_date=datetime.now(), news_category_id=1,
                           is_approved=False, checked=True)
        news_object.save_to_db()

        journalist_news_object = JournalistNewsMapping(journalist_id=user_object.id, news_id=news_object.news_id)
        journalist_news_object.save_to_db()

        user_object = User(name="User", email="user@gmail.com", password=password,
                           user_type_id=3)
        user_object.save_to_db()

        user_object = User(name="Dhruv", email="dhruv@gmail.com", password=password,
                           has_premium=True, user_type_id=3)
        user_object.save_to_db()

        return user_object
