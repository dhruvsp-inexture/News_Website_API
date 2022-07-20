import cloudinary
import datetime
from flask import request
from flask_api import status
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource
from sqlalchemy.exc import DataError
from app import db
from journalist.models import News, NewsCategory, JournalistNewsMapping
from journalist.utils import journalist_required
import cloudinary.uploader


class PostArticle(Resource):
    decorators = [jwt_required(), journalist_required()]

    def post(self):
        article_data = request.form

        try:
            news_category = NewsCategory.query.filter_by(category=article_data["category"].title()).first()
            if not news_category:
                return {"data": [],
                        "message": "please enter valid category",
                        "status": "false"
                        }, status.HTTP_400_BAD_REQUEST
            if request.files.get("image"):
                picture = request.files.get("image")
                upload_result = cloudinary.uploader.upload(picture, folder="News_Website_API")
                picture = upload_result["url"]
            else:
                picture = None
            news = News(news_heading=article_data["news_heading"], news_info=article_data["news_info"],
                        news_category_id=news_category.category_id, image=picture)
            news.save_to_db()
            journalist = JournalistNewsMapping(news_id=news.news_id, journalist_id=get_jwt_identity())
            journalist.save_to_db()
            return {"data": [],
                    "message": "News posted successfully",
                    "status": "true"
                    }, status.HTTP_201_CREATED
        except (KeyError, AttributeError) as err:
            return {"data": [],
                    "message": "Please enter proper data",
                    "status": "false"
                    }, status.HTTP_400_BAD_REQUEST


class ShowMyArticles(Resource):
    decorators = [jwt_required(), journalist_required()]

    def get(self):
        news_data = {}
        journalist_mapping_obj = JournalistNewsMapping.query.filter_by(journalist_id=get_jwt_identity()).all()
        for journalist in journalist_mapping_obj:
            news = News.query.filter_by(news_id=journalist.news_id).first()
            news_obj_news_id = news.news_id
            news_data[news_obj_news_id] = {}
            news_data[news_obj_news_id]["news_heading"] = news.news_heading
            news_data[news_obj_news_id]["news_info"] = news.news_info
            news_data[news_obj_news_id]["date"] = news.news_date
            news_data[news_obj_news_id]["checked"] = news.checked
            news_data[news_obj_news_id]["is_approved"] = news.is_approved
            news_data[news_obj_news_id]["image"] = news.image
            news_category = NewsCategory.query.filter_by(category_id=news.news_category_id).first()
            news_data[news_obj_news_id]["category"] = news_category.category
        return {"data": news_data,
                "message": "Articles fetched successfully",
                "status": "true"
                }, status.HTTP_200_OK


class UpdateArticle(Resource):
    decorators = [jwt_required(), journalist_required()]

    def put(self):
        update_article_data = request.get_json()
        try:
            journalist_mapping_obj = JournalistNewsMapping.query.filter_by(journalist_id=get_jwt_identity(),
                                                                           news_id=update_article_data["id"]).first()
            if not journalist_mapping_obj:
                return {"data": [],
                        "message": "Invalid Id",
                        "status": "false"
                        }, status.HTTP_404_NOT_FOUND
            news_obj = News.query.filter_by(news_id=journalist_mapping_obj.news_id, checked=False).first()
            if not news_obj:
                return {"data": [],
                        "message": "Invalid Id",
                        "status": "false"
                        }, status.HTTP_404_NOT_FOUND
            news_obj.news_heading = update_article_data["news_heading"]
            news_obj.news_info = update_article_data["news_info"]
            news_obj.news_date = datetime.datetime.today()
            db.session.commit()
            return {"data": [],
                    "message": "Article updated successfully",
                    "status": "true"
                    }, status.HTTP_200_OK
        except (KeyError, AttributeError, DataError) as err:
            return {"data": [],
                    "message": "Please enter proper data",
                    "status": "false"
                    }, status.HTTP_400_BAD_REQUEST


class DeleteArticle(Resource):
    decorators = [jwt_required(), journalist_required()]

    def delete(self):
        delete_article_data = request.get_json()

        try:
            journalist_mapping_obj = JournalistNewsMapping.query.filter_by(journalist_id=get_jwt_identity(),
                                                                           news_id=delete_article_data["id"]).first()
            if not journalist_mapping_obj:
                return {"data": [],
                        "message": "Invalid Id",
                        "status": "false"
                        }, status.HTTP_404_NOT_FOUND
            db.session.delete(journalist_mapping_obj)
            db.session.commit()
            news_obj = News.query.filter_by(news_id=delete_article_data["id"]).first()
            db.session.delete(news_obj)
            db.session.commit()
            return {"data": [],
                    "message": "Article deleted successfully",
                    "status": "true"
                    }, status.HTTP_200_OK

        except (KeyError, AttributeError, DataError) as err:
            return {"data": [],
                    "message": "Please enter proper data",
                    "status": "false"
                    }, status.HTTP_400_BAD_REQUEST
