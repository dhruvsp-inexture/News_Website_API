from flask import Blueprint

from journalist.resources import PostArticle, ShowMyArticles, UpdateArticle, DeleteArticle

journalist = Blueprint("journalist", __name__)

journalist.add_url_rule("/journalist/post_article", view_func=PostArticle.as_view("post_article"))
journalist.add_url_rule("/journalist/show_my_articles", view_func=ShowMyArticles.as_view("show_my_articles"))
journalist.add_url_rule("/journalist/update_article", view_func=UpdateArticle.as_view("update_article"))
journalist.add_url_rule("/journalist/delete_article", view_func=DeleteArticle.as_view("delete_article"))