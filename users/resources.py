from flask_api import status
from flask_restful import Resource
from flask import request
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from sqlalchemy.exc import DataError
from app import db, bcrypt
from journalist.models import JournalistNewsMapping, News, NewsCategory
from users.models import User
from users.utils import send_reset_email
from users.validations import validate_name, validate_email, validate_password


class Registration(Resource):

    def post(self):
        user_json = request.get_json()
        try:
            user = User.query.filter_by(email=user_json['email']).first()
            if user:
                return {"data": [],
                        "message": "user with this email id already exists please choose different email",
                        "status": "false"
                        }, status.HTTP_400_BAD_REQUEST

            if not validate_name(user_json['name']):
                return {"data": [],
                        "message": "Please enter proper name",
                        "status": "false"
                        }, status.HTTP_400_BAD_REQUEST

            if not validate_email(user_json["email"]):
                return {"data": [],
                        "message": "Please enter proper email",
                        "status": "false"
                        }, status.HTTP_400_BAD_REQUEST

            if not validate_password(user_json["password"]):
                return {"data": [],
                        "message": "Please enter proper password",
                        "status": "false"
                        }, status.HTTP_400_BAD_REQUEST
            hashed_password = bcrypt.generate_password_hash(user_json['password']).decode('utf-8')
            user_object = User(name=user_json['name'], email=user_json['email'], password=hashed_password,
                               user_type_id=user_json['user_type_id'])
            user_object.save_to_db()
            return {"data": request.get_json(), "message": "User Register Successfully",
                    "status": "true"}, status.HTTP_201_CREATED
        except (KeyError, AttributeError, DataError) as err:
            return {"data": [],
                    "message": "Please enter proper data",
                    "status": "false"
                    }, status.HTTP_400_BAD_REQUEST


class Login(Resource):

    def post(self):
        login_json_data = request.get_json()
        try:
            user = User.query.filter_by(email=login_json_data["email"]).first()
            if not user:
                return {"data": [],
                        "message": "email doesn't exists",
                        "status": "false"
                        }, status.HTTP_404_NOT_FOUND
            if bcrypt.check_password_hash(user.password, login_json_data["password"]):
                access_token = create_access_token(identity=user.id)
                return {"message": "Login Successfully",
                        "data": {"access_token": access_token},
                        "status": "true"
                        }, status.HTTP_200_OK
            else:
                return {"data": [],
                        "message": "Invalid password",
                        "status": "false"
                        }, status.HTTP_400_BAD_REQUEST
        except (KeyError, AttributeError) as err:
            return {"data": [],
                    "message": "Please enter proper data",
                    "status": "false"
                    }, status.HTTP_400_BAD_REQUEST


class Profile(Resource):
    decorators = [jwt_required()]

    def get(self):
        user = User.query.filter_by(id=get_jwt_identity()).first()
        return {"data": {"name": user.name, "email": user.email, "has_premium": user.has_premium},
                "message": "user data fetched successfully",
                "status": "true"
                }, status.HTTP_200_OK


class UpdateProfile(Resource):
    decorators = [jwt_required()]

    def put(self):
        profile_json_data = request.get_json()
        user = User.query.filter_by(id=get_jwt_identity()).first()
        try:
            user_obj = User.query.filter(User.email == profile_json_data['email'], User.id != user.id).first()
            if user_obj:
                return {"data": [],
                        "message": "user with this email id already exists please choose different email",
                        "status": "false"
                        }, status.HTTP_400_BAD_REQUEST
            if not validate_name(profile_json_data['name']):
                return {"data": [],
                        "message": "Please enter proper name",
                        "status": "false"
                        }, status.HTTP_400_BAD_REQUEST

            if not validate_email(profile_json_data["email"]):
                return {"data": [],
                        "message": "Please enter proper email",
                        "status": "false"
                        }, status.HTTP_400_BAD_REQUEST
            user.name = profile_json_data["name"]
            user.email = profile_json_data["email"]
            db.session.commit()
        except (KeyError, AttributeError, DataError) as err:
            return {"data": [],
                    "message": "Please enter proper data",
                    "status": "false"
                    }, status.HTTP_400_BAD_REQUEST
        return {"data": [],
                "message": "Profile Updated Successfully",
                "status": "true"
                }, status.HTTP_200_OK


class ChangePassword(Resource):
    decorators = [jwt_required()]

    def post(self):
        password_json_data = request.get_json()
        user = User.query.filter_by(id=get_jwt_identity()).first()
        try:
            # if password_json_data["current_password"] == user.password:
            if bcrypt.check_password_hash(user.password, password_json_data["current_password"]):
                if not validate_password(password_json_data["new_password"]):
                    return {"data": [],
                            "message": "Please enter proper password",
                            "status": "false"
                            }, status.HTTP_400_BAD_REQUEST

                user.password = bcrypt.generate_password_hash(password_json_data["new_password"]).decode('utf-8')
                db.session.commit()
            else:
                return {"data": [],
                        "message": "Invalid current password",
                        "status": "false"
                        }, status.HTTP_400_BAD_REQUEST
        except (KeyError, AttributeError) as err:
            return {"data": [],
                    "message": "Please enter proper data",
                    "status": "false"
                    }, status.HTTP_400_BAD_REQUEST
        return {"data": [],
                "message": "Password changed successfully",
                "status": "true"
                }, status.HTTP_200_OK


class ShowArticles(Resource):

    def get(self):
        news_json = {}
        news_data_obj = News.query.filter_by(is_approved=True)
        for news in news_data_obj:
            news_obj_news_id = news.news_id
            news_json[news_obj_news_id] = {}
            journalist_mapping_obj = JournalistNewsMapping.query.filter_by(news_id=news_obj_news_id).first()
            news_json[news_obj_news_id]["journalist_id"] = journalist_mapping_obj.journalist_id
            news_json[news_obj_news_id]["news_info"] = news.news_info
            news_json[news_obj_news_id]["news_heading"] = news.news_heading
            news_json[news_obj_news_id]["news_date"] = news.news_date
            news_json[news_obj_news_id]["news_image"] = news.image
            category_obj = NewsCategory.query.filter_by(category_id=news.news_category_id).first()
            news_json[news_obj_news_id]["news_category"] = category_obj.category
        return {"data": news_json,
                "message": "Articles fetched successfully",
                "status": "true"
                }, status.HTTP_200_OK


class ResetPasswordRequest(Resource):
    """class for getting the home page if user is already logged in and posting the data"""

    def post(self):
        """method for checking if the email is valid """
        reset_request_json = request.get_json()
        try:
            user = User.query.filter_by(email=reset_request_json["email"]).first()
            if user:
                token = send_reset_email(user)
                return {"data": token,
                        "message": "An email has been sent to your id please check it to reset your password.",
                        "status": "true"
                        }, status.HTTP_200_OK
            return {"data": [],
                    "message": "Invalid email id. Please enter valid email.",
                    "status": "false"
                    }, status.HTTP_404_NOT_FOUND

        except KeyError as err:
            return {"data": [],
                    "message": "Enter proper data",
                    "status": "False"
                    }, status.HTTP_400_BAD_REQUEST


class ResetPassword(Resource):
    """class for getting the home page if the user is already logged in and posting the data of the user after the
     password reset"""

    def post(self):
        """method for verifying the token to reset the password and creating new password for the user"""
        reset_password_json = request.get_json()

        try:
            user = User.verify_reset_token(reset_password_json["token"])
            if user is None:
                return {"data": [],
                        "message": "That is an invalid or expired token",
                        "status": "false"
                        }, status.HTTP_400_BAD_REQUEST
            if not validate_password(reset_password_json["password"]):
                return {"data": [],
                        "message": "Please enter proper password",
                        "status": "false"
                        }, status.HTTP_400_BAD_REQUEST
            hashed_password = bcrypt.generate_password_hash(reset_password_json["password"]).decode('utf-8')
            user.password = hashed_password
            db.session.commit()
            return {"data": [],
                    "message": "Your password has been updated! You can now log in",
                    "status": "true"
                    }, status.HTTP_200_OK

        except KeyError as err:
            return {"data": [],
                    "message": "Enter proper data",
                    "status": "false"
                    }, status.HTTP_400_BAD_REQUEST
