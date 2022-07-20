from flask import Blueprint
from users.resources import Registration, Login, Profile, UpdateProfile, ChangePassword, ShowArticles, \
    ResetPasswordRequest, ResetPassword

users = Blueprint("users", __name__)

users.add_url_rule("/registration", view_func=Registration.as_view("registration"))
users.add_url_rule("/login", view_func=Login.as_view("login"))
users.add_url_rule("/profile", view_func=Profile.as_view("profile"))
users.add_url_rule("/update_profile", view_func=UpdateProfile.as_view("update_profile"))
users.add_url_rule("/change_password", view_func=ChangePassword.as_view("change_password"))
users.add_url_rule("/show_articles", view_func=ShowArticles.as_view("show_articles"))
users.add_url_rule("/reset_password_request", view_func=ResetPasswordRequest.as_view("reset_password_request"))
users.add_url_rule("/reset_password", view_func=ResetPassword.as_view("reset_password"))
