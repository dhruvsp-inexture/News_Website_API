import os
from flask import Flask
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from config import Config
from flask_mail import Mail

bcrypt = Bcrypt()
db = SQLAlchemy()
mail = Mail()


def create_app(config_class=Config, **kwargs):
    app = Flask(__name__)
    app.config["SECRET_KEY"] = os.environ.get('SECRET_KEY')
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("SQLALCHEMY_DATABASE_URI")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config['PROPAGATE_EXCEPTIONS'] = True
    app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USERNAME'] = os.environ.get('EMAIL_USER')
    app.config['MAIL_PASSWORD'] = os.environ.get('EMAIL_PASS')

    mail.init_app(app)
    bcrypt.init_app(app)
    db.init_app(app)
    from users import models
    from journalist import models
    from public import models
    jwt = JWTManager(app)

    Migrate(app, db)
    db.init_app(app)

    from main.routes import main
    from users.routes import users
    from journalist.routes import journalist
    from admin.routes import admin
    from public.routes import public
    app.register_blueprint(main)
    app.register_blueprint(users)
    app.register_blueprint(journalist)
    app.register_blueprint(admin)
    app.register_blueprint(public)

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
