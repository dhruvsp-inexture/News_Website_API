import json

from tests.test_journalist.test_journalist import test_journalist_login_success


def test_admin_login_success(client, db, user):
    login_data = {"email": "admin@gmail.com", "password": "abc"}
    response = client.post("/login", data=json.dumps(login_data), content_type="application/json")
    assert response.json["message"] == "Login Successfully"
    assert response.json["status"] == "true"
    assert response.status_code == 200
    return f'Bearer {response.json["data"]["access_token"]}'


def test_get_all_categories_success(client, db, user):
    access_token = test_admin_login_success(client, db, user)
    response = client.get('/admin/show_all_categories', headers={"Authorization": access_token})
    assert response.json["message"] == "Categories fetched successfully"
    assert response.json["status"] == "true"
    assert response.status_code == 200


def test_add_category_success(client, db, user):
    access_token = test_admin_login_success(client, db, user)
    add_category_data = {"category": "Sports"}
    response = client.post('/admin/add_category', headers={"Authorization": access_token},
                           data=json.dumps(add_category_data), content_type="application/json")
    assert response.json["message"] == "Category Added Successfully"
    assert response.json["status"] == "true"
    assert response.status_code == 201


def test_add_category_already_exists(client, db, user):
    access_token = test_admin_login_success(client, db, user)
    add_category_data = {"category": "General"}
    response = client.post('/admin/add_category', headers={"Authorization": access_token},
                           data=json.dumps(add_category_data), content_type="application/json")
    assert response.json["message"] == "Category already exists"
    assert response.json["status"] == "false"
    assert response.status_code == 400


def test_add_category_invalid_data(client, db, user):
    access_token = test_admin_login_success(client, db, user)
    add_category_data = {"categoryyy": "Sports"}
    response = client.post('/admin/add_category', headers={"Authorization": access_token},
                           data=json.dumps(add_category_data), content_type="application/json")
    assert response.json["message"] == "Please enter proper data"
    assert response.json["status"] == "false"
    assert response.status_code == 400


def test_get_all_articles(client, db, user):
    access_token = test_admin_login_success(client, db, user)
    response = client.get("/admin/show_all_articles", headers={"Authorization": access_token})
    assert response.json["message"] == "data fetched successfully"
    assert response.json["status"] == "true"
    assert response.status_code == 200


def test_get_all_articles_admin_required(client, db, user):
    access_token = test_journalist_login_success(client, db, user)
    response = client.get('/admin/show_all_articles', headers={"Authorization": access_token})
    assert response.json["msg"] == "Admins only!"
    assert response.json["status"] == "false"
    assert response.status_code == 403


def test_approve_articles_success(client, db, user):
    access_token = test_admin_login_success(client, db, user)
    approve_articles_data = {"id": 1}
    response = client.post('/admin/approve_articles', headers={"Authorization": access_token},
                           data=json.dumps(approve_articles_data), content_type="application/json")
    assert response.json["message"] == "Article approved!!!"
    assert response.json["status"] == "true"
    assert response.status_code == 200


def test_approve_articles_invalid_id(client, db, user):
    access_token = test_admin_login_success(client, db, user)
    approve_articles_data = {"id": "abc"}
    response = client.post('/admin/approve_articles', headers={"Authorization": access_token},
                           data=json.dumps(approve_articles_data), content_type="application/json")
    assert response.json["message"] == "invalid id"
    assert response.json["status"] == "false"
    assert response.status_code == 404


def test_approve_articles_invalid_data(client, db, user):
    access_token = test_admin_login_success(client, db, user)
    approve_articles_data = {"iddd": 1}
    response = client.post('/admin/approve_articles', headers={"Authorization": access_token},
                           data=json.dumps(approve_articles_data), content_type="application/json")
    assert response.json["message"] == "Please enter proper data"
    assert response.json["status"] == "false"
    assert response.status_code == 400


def test_decline_articles_success(client, db, user):
    access_token = test_admin_login_success(client, db, user)
    decline_articles_data = {"id": 1}
    response = client.post('/admin/decline_articles', headers={"Authorization": access_token},
                           data=json.dumps(decline_articles_data), content_type="application/json")
    assert response.json["message"] == "Article declined!!!"
    assert response.json["status"] == "true"
    assert response.status_code == 200


def test_decline_articles_invalid_id(client, db, user):
    access_token = test_admin_login_success(client, db, user)
    decline_articles_data = {"id": "abc"}
    response = client.post('/admin/decline_articles', headers={"Authorization": access_token},
                           data=json.dumps(decline_articles_data), content_type="application/json")
    assert response.json["message"] == "invalid id"
    assert response.json["status"] == "false"
    assert response.status_code == 404


def test_decline_articles_invalid_data(client, db, user):
    access_token = test_admin_login_success(client, db, user)
    decline_articles_data = {"iddd": 1}
    response = client.post('/admin/decline_articles', headers={"Authorization": access_token},
                           data=json.dumps(decline_articles_data), content_type="application/json")
    assert response.json["message"] == "Please enter proper data"
    assert response.json["status"] == "false"
    assert response.status_code == 400


def test_delete_category_success(client, db, user):
    access_token = test_admin_login_success(client, db, user)
    delete_category_data = {"id": "2"}
    response = client.delete('/admin/delete_category', headers={"Authorization": access_token},
                             data=json.dumps(delete_category_data), content_type="application/json")
    assert response.json["message"] == "category deleted successfully"
    assert response.json["status"] == "true"
    assert response.status_code == 200


def test_delete_category_news_exists(client, db, user):
    access_token = test_admin_login_success(client, db, user)
    delete_category_data = {"id": "1"}
    response = client.delete('/admin/delete_category', headers={"Authorization": access_token},
                             data=json.dumps(delete_category_data), content_type="application/json")
    assert response.json["message"] == "news already exists for this category you can't delete it"
    assert response.json["status"] == "false"
    assert response.status_code == 400


def test_delete_category_invalid_id(client, db, user):
    access_token = test_admin_login_success(client, db, user)
    delete_category_data = {"id": "abc"}
    response = client.delete('/admin/delete_category', headers={"Authorization": access_token},
                             data=json.dumps(delete_category_data), content_type="application/json")
    assert response.json["message"] == "enter valid id"
    assert response.json["status"] == "false"
    assert response.status_code == 404


def test_delete_category_invalid_data(client, db, user):
    access_token = test_admin_login_success(client, db, user)
    delete_category_data = {"iddd": "1"}
    response = client.delete('/admin/delete_category', headers={"Authorization": access_token},
                             data=json.dumps(delete_category_data), content_type="application/json")
    assert response.json["message"] == "Please enter proper data"
    assert response.json["status"] == "false"
    assert response.status_code == 400
