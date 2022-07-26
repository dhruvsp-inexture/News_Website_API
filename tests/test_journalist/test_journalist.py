import json

from tests.test_users.test_users import test_login_success


def test_journalist_login_success(client, db, user):
    login_data = {"email": "journalist@gmail.com", "password": "abc"}
    response = client.post("/login", data=json.dumps(login_data), content_type="application/json")
    assert response.json["message"] == "Login Successfully"
    assert response.json["status"] == "true"
    assert response.status_code == 200
    return f'Bearer {response.json["data"]["access_token"]}'


def test_post_article_invalid_category(client, db, user):
    access_token = test_journalist_login_success(client, db, user)
    fp = 'C:/Wallpapers/goku_2020_4k_hd.jpg'

    post_article_data = {"news_heading": "First testing heading article",
                         "news_info": "Content of the first testing article", "category": "Politics",
                         "image": open(fp, "rb")}
    response = client.post("/journalist/post_article", data=post_article_data, headers={"Authorization": access_token},
                           content_type="multipart/form-data")
    assert response.json["message"] == "please enter valid category"
    assert response.json["status"] == "false"
    assert response.status_code == 400


def test_post_article_invalid_data(client, db, user):
    access_token = test_journalist_login_success(client, db, user)
    fp = 'C:/Wallpapers/goku_2020_4k_hd.jpg'

    post_article_data = {"news_headinggg": "First testing heading article",
                         "news_infooo": "Content of the first testing article", "categoryyy": "General",
                         "imageee": open(fp, "rb")}
    response = client.post("/journalist/post_article", data=post_article_data, headers={"Authorization": access_token},
                           content_type="multipart/form-data")
    assert response.json["message"] == "Please enter proper data"
    assert response.json["status"] == "false"
    assert response.status_code == 400


def test_post_article_with_image_success(client, db, user):
    access_token = test_journalist_login_success(client, db, user)
    fp = 'C:/Wallpapers/goku_2020_4k_hd.jpg'

    post_article_data = {"news_heading": "First testing heading article",
                         "news_info": "Content of the first testing article", "category": "General",
                         "image": open(fp, "rb")}
    response = client.post("/journalist/post_article", data=post_article_data, headers={"Authorization": access_token},
                           content_type="multipart/form-data")
    assert response.json["message"] == "News posted successfully"
    assert response.json["status"] == "true"
    assert response.status_code == 201


def test_post_article_without_image_success(client, db, user):
    access_token = test_journalist_login_success(client, db, user)

    post_article_data = {"news_heading": "First testing heading article without image",
                         "news_info": "Content of the first testing article without image", "category": "General"}
    response = client.post("/journalist/post_article", data=post_article_data, headers={"Authorization": access_token},
                           content_type="multipart/form-data")
    assert response.json["message"] == "News posted successfully"
    assert response.json["status"] == "true"
    assert response.status_code == 201


def test_show_my_articles(client, db, user):
    access_token = test_journalist_login_success(client, db, user)
    response = client.get('/journalist/show_my_articles', headers={"Authorization": access_token})
    assert response.json["message"] == "Articles fetched successfully"
    assert response.json["status"] == "true"
    assert response.status_code == 200


def test_show_my_articles_journalist_required(client, db, user):
    access_token = test_login_success(client, db, user)
    response = client.get('/journalist/show_my_articles', headers={"Authorization": access_token})
    assert response.json["msg"] == "Journalists only!"
    assert response.json["status"] == "false"
    assert response.status_code == 403


def test_update_article_success(client, db, user):
    access_token = test_journalist_login_success(client, db, user)
    udpate_article_data = {"id": "1", "news_heading": "Updated heading", "news_info": "updated content"}
    response = client.put("/journalist/update_article", headers={"Authorization": access_token},
                          data=json.dumps(udpate_article_data), content_type="application/json")
    assert response.json["message"] == "Article updated successfully"
    assert response.json["status"] == "true"
    assert response.status_code == 200


def test_update_checked_article_fail(client, db, user):
    access_token = test_journalist_login_success(client, db, user)
    udpate_article_data = {"id": "2", "news_heading": "Updated heading", "news_info": "updated content"}
    response = client.put("/journalist/update_article", headers={"Authorization": access_token},
                          data=json.dumps(udpate_article_data), content_type="application/json")
    assert response.json["message"] == "Invalid Id"
    assert response.json["status"] == "false"
    assert response.status_code == 404


def test_update_article_invalid_id(client, db, user):
    access_token = test_journalist_login_success(client, db, user)
    udpate_article_data = {"id": "abc", "news_heading": "Updated heading", "news_info": "updated content"}
    response = client.put("/journalist/update_article", headers={"Authorization": access_token},
                          data=json.dumps(udpate_article_data), content_type="application/json")
    assert response.json["message"] == "Invalid Id"
    assert response.json["status"] == "false"
    assert response.status_code == 404


def test_update_article_invalid_data(client, db, user):
    access_token = test_journalist_login_success(client, db, user)
    udpate_article_data = {"iddd": "1", "news_headinggg": "Updated headinggg", "news_infooo": "updated content"}
    response = client.put("/journalist/update_article", headers={"Authorization": access_token},
                          data=json.dumps(udpate_article_data), content_type="application/json")
    assert response.json["message"] == "Please enter proper data"
    assert response.json["status"] == "false"
    assert response.status_code == 400


def test_delete_article_success(client, db, user):
    access_token = test_journalist_login_success(client, db, user)
    delete_article_data = {"id": 1}
    response = client.delete('/journalist/delete_article', headers={"Authorization": access_token},
                             data=json.dumps(delete_article_data), content_type="application/json")
    assert response.json["message"] == "Article deleted successfully"
    assert response.json["status"] == "true"
    assert response.status_code == 200


def test_delete_article_invalid_id(client, db, user):
    access_token = test_journalist_login_success(client, db, user)
    delete_article_data = {"id": "abc"}
    response = client.delete('/journalist/delete_article', headers={"Authorization": access_token},
                             data=json.dumps(delete_article_data), content_type="application/json")
    assert response.json["message"] == "Invalid Id"
    assert response.json["status"] == "false"
    assert response.status_code == 404


def test_delete_article_invalid_data(client, db, user):
    access_token = test_journalist_login_success(client, db, user)
    delete_article_data = {"iddd": 1}
    response = client.delete('/journalist/delete_article', headers={"Authorization": access_token},
                             data=json.dumps(delete_article_data), content_type="application/json")
    assert response.json["message"] == "Please enter proper data"
    assert response.json["status"] == "false"
    assert response.status_code == 400
