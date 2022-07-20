from flask import request
from flask_api import status
from flask_jwt_extended import jwt_required
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError, DataError
from admin.utils import admin_required
from app import db
from journalist.models import News, JournalistNewsMapping, NewsCategory


class ShowAllArticles(Resource):
    decorators = [jwt_required(), admin_required()]

    def get(self):
        news_json = {}
        news_data_obj = News.query.all()
        for news in news_data_obj:
            data_news_id = news.news_id
            news_json[data_news_id] = {}
            journalist_mapping_obj = JournalistNewsMapping.query.filter_by(news_id=data_news_id).first()
            news_json[data_news_id]["journalist_id"] = journalist_mapping_obj.journalist_id
            news_json[data_news_id]["news_info"] = news.news_info
            news_json[data_news_id]["news_heading"] = news.news_heading
            news_json[data_news_id]["news_date"] = news.news_date
            category_obj = NewsCategory.query.filter_by(category_id=news.news_category_id).first()
            news_json[data_news_id]["news_category"] = category_obj.category
            news_json[data_news_id]["checked"] = news.checked
            news_json[data_news_id]["is_approved"] = news.is_approved
        return {
                   "data": news_json,
                   "message": "data fetched successfully",
                   "status": "true"
               }, status.HTTP_200_OK


class ApproveArticles(Resource):
    decorators = [jwt_required(), admin_required()]

    def post(self):
        approve_article_id_json = request.get_json()
        try:
            news = News.query.filter_by(news_id=approve_article_id_json["id"], checked=False).first()
            if news:
                news.is_approved = True
                news.checked = True
                db.session.commit()
                return {"data": [],
                        "message": "Article approved!!!",
                        "status": "true"
                        }, status.HTTP_200_OK
            return {"data": [],
                    "message": "invalid id",
                    "status": "false"
                    }, status.HTTP_404_NOT_FOUND
        except (KeyError, AttributeError, DataError) as err:
            return {"data": [],
                    "message": "Please enter proper data",
                    "status": "false"
                    }, status.HTTP_400_BAD_REQUEST


class DeclineArticles(Resource):
    decorators = [jwt_required(), admin_required()]

    def post(self):
        approve_article_id_json = request.get_json()
        try:
            news = News.query.filter_by(news_id=approve_article_id_json["id"], checked=False).first()
            if news:
                news.is_approved = False
                news.checked = True
                db.session.commit()
                return {"data": [],
                        "message": "Article declined!!!",
                        "status": "true"
                        }, status.HTTP_200_OK
            return {"data": [],
                    "message": "invalid id",
                    "status": "false"
                    }, status.HTTP_404_NOT_FOUND
        except (KeyError, AttributeError, DataError) as err:
            return {"data": [],
                    "message": "Please enter proper data",
                    "status": "false"
                    }, status.HTTP_400_BAD_REQUEST


class ShowAllCategories(Resource):
    decorators = [jwt_required(), admin_required()]

    def get(self):
        category_json = {}
        category_obj = NewsCategory.query.all()
        for category in category_obj:
            category_json[category.category_id] = category.category
        return {"data": category_json,
                "message": "Categories fetched successfully",
                "status": "true"
                }, status.HTTP_200_OK


class AddCategory(Resource):
    decorators = [jwt_required(), admin_required()]

    def post(self):
        add_category_json = request.get_json()
        try:
            category_obj = NewsCategory.query.filter_by(category=add_category_json["category"].title()).first()
            if not category_obj:
                add_category = NewsCategory(category=add_category_json["category"])
                add_category.save_to_db()
                return {"data": [],
                        "message": "Category Added Successfully",
                        "status": "true"
                        }, status.HTTP_201_CREATED
            return {"data": [],
                    "message": "Category already exists",
                    "status": "false"
                    }, status.HTTP_400_BAD_REQUEST
        except (KeyError, AttributeError, IntegrityError, DataError) as err:
            return {"data": [],
                    "message": "Please enter proper data",
                    "status": "false"
                    }, status.HTTP_400_BAD_REQUEST


class DeleteCategory(Resource):
    decorators = [jwt_required(), admin_required()]

    def delete(self):
        delete_category_json = request.get_json()
        try:
            category_obj = NewsCategory.query.filter_by(category_id=delete_category_json["id"]).first()
            if category_obj:
                news_obj = News.query.filter_by(news_category_id=delete_category_json["id"]).first()
                if news_obj:
                    return {"data": [],
                            "message": "news already exists for this category you can't delete it",
                            "status": "false"
                            }, status.HTTP_400_BAD_REQUEST
                db.session.delete(category_obj)
                db.session.commit()
                return {"data": [],
                        "message": "category deleted successfully",
                        "status": "true"
                        }, status.HTTP_200_OK

            return {"data": [],
                    "message": "enter valid id",
                    "status": "false"
                    }, status.HTTP_404_NOT_FOUND
        except (KeyError, AttributeError, DataError) as err:
            return {"data": [],
                    "message": "Please enter proper data",
                    "status": "false"
                    }, status.HTTP_400_BAD_REQUEST
