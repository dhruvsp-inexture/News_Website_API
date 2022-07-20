from flask import Blueprint
from admin.resources import ShowAllArticles, ApproveArticles, DeclineArticles, ShowAllCategories, AddCategory, \
    DeleteCategory

admin = Blueprint("admin_portal", __name__)

admin.add_url_rule("/admin/show_all_articles", view_func=ShowAllArticles.as_view("show_all_articles"))
admin.add_url_rule("/admin/approve_articles", view_func=ApproveArticles.as_view("approve_articles"))
admin.add_url_rule("/admin/decline_articles", view_func=DeclineArticles.as_view("decline_articles"))
admin.add_url_rule("/admin/show_all_categories", view_func=ShowAllCategories.as_view("show_all_categories"))
admin.add_url_rule("/admin/add_category", view_func=AddCategory.as_view("add_category"))
admin.add_url_rule("/admin/delete_category", view_func=DeleteCategory.as_view("delete_category"))
