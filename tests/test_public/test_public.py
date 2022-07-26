import json

from tests.test_users.test_users import test_login_success


def test_public_login_success(client, db, user):
    login_data = {"email": "user@gmail.com", "password": "abc"}
    response = client.post("/login", data=json.dumps(login_data), content_type="application/json")
    assert response.json["message"] == "Login Successfully"
    assert response.json["status"] == "true"
    assert response.status_code == 200
    return f'Bearer {response.json["data"]["access_token"]}'


def test_buy_subscription_success(client, db, user):
    access_token = test_public_login_success(client, db, user)
    response = client.get("/buy_subscription", headers={"Authorization": access_token})
    assert response.json["message"] == "click on following link to complete the payment"
    assert response.json["status"] == "true"
    assert response.status_code == 200


def test_buy_subscription_public_required(client, db, user):
    access_token = test_login_success(client, db, user)
    response = client.get("/buy_subscription", headers={"Authorization": access_token})
    assert response.json["msg"] == "Public only!"
    assert response.json["status"] == "false"
    assert response.status_code == 403


def test_subscription_already_bought(client, db, user):
    login_data = {"email": "dhruv@gmail.com", "password": "abc"}
    response = client.post("/login", data=json.dumps(login_data), content_type="application/json")
    access_token = f'Bearer {response.json["data"]["access_token"]}'
    response = client.get("/buy_subscription", headers={"Authorization": access_token})
    assert response.json["message"] == "Subscription already purchased"
    assert response.json["status"] == "false"
    assert response.status_code == 400


def test_payment_success(client, db, user):
    access_token = test_public_login_success(client, db, user)
    response = client.get("/success", headers={"Authorization": access_token})
    assert response.json["message"] == "Congrats, now you are a premium user!!!"
    assert response.json["status"] == "true"
    assert response.status_code == 200


def test_payment_cancel(client, db, user):
    access_token = test_public_login_success(client, db, user)
    response = client.get("/cancel", headers={"Authorization": access_token})
    assert response.json["message"] == "Payment Cancelled. Please try again!"
    assert response.json["status"] == "true"
    assert response.status_code == 200
