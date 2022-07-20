from flask import Blueprint
from main.resources import HomePage

main = Blueprint("main", __name__)
main.add_url_rule("/", view_func=HomePage.as_view("home"))
main.add_url_rule("/home", view_func=HomePage.as_view("home_page"))
