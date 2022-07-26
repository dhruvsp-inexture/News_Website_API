import json


def test_get_home_page(client):
    response = client.get("/home")

    assert response.status_code == 200
    assert response.json["data"] == "Hello World!"
    assert response.json["message"] == "Home Page"
    assert response.json["status"] == "true"


def test_login_success(client, db, user):
    login_data = {"email": "admin@gmail.com", "password": "abc"}
    response = client.post("/login", data=json.dumps(login_data), content_type="application/json")
    assert response.json["message"] == "Login Successfully"
    assert response.json["status"] == "true"
    assert response.status_code == 200
    return f'Bearer {response.json["data"]["access_token"]}'


def test_login_invalid_keys(client, db, user):
    login_data = {"emailsssss": "admin@gmail.com", "password": "abc"}
    response = client.post("/login", data=json.dumps(login_data), content_type="application/json")
    assert response.json["message"] == "Please enter proper data"
    assert response.json["status"] == "false"
    assert response.status_code == 400


def test_login_invalid_email(client, db, user):
    login_data = {"email": "admin123@gmail.com", "password": "abc"}
    response = client.post("/login", data=json.dumps(login_data), content_type="application/json")
    assert response.json["message"] == "email doesn't exists"
    assert response.json["status"] == "false"
    assert response.status_code == 404


def test_login_invalid_password(client, db, user):
    login_data = {"email": "admin@gmail.com", "password": "123"}
    response = client.post("/login", data=json.dumps(login_data), content_type="application/json")
    assert response.json["message"] == "Invalid password"
    assert response.json["status"] == "false"
    assert response.status_code == 400


def test_registration_success(client, db, user):
    register_data = {"name": "abc", "email": "abc@gmail.com", "password": "Abc@123", "user_type_id": 1}
    response = client.post("/registration", data=json.dumps(register_data), content_type="application/json")
    assert response.json["data"] == register_data
    assert response.json["message"] == "User Register Successfully"
    assert response.json["status"] == "true"
    assert response.status_code == 201


def test_registration_fail_email_already_exists(client, db, user):
    register_data = {"name": "abc", "email": "admin@gmail.com", "password": "Abc@123", "user_type_id": 1}
    response = client.post("/registration", data=json.dumps(register_data), content_type="application/json")
    assert response.json["message"] == "user with this email id already exists please choose different email"
    assert response.json["status"] == "false"
    assert response.status_code == 400


def test_registration_fail_invalid_name(client, db, user):
    register_data = {"name": "abc123", "email": "abc@gmail.com", "password": "Abc@123", "user_type_id": 1}
    response = client.post("/registration", data=json.dumps(register_data), content_type="application/json")
    assert response.json["message"] == "Please enter proper name"
    assert response.json["status"] == "false"
    assert response.status_code == 400


def test_registration_fail_invalid_email(client, db, user):
    register_data = {"name": "abc", "email": "@gmail.com", "password": "Abc@123", "user_type_id": 1}
    response = client.post("/registration", data=json.dumps(register_data), content_type="application/json")
    assert response.json["message"] == "Please enter proper email"
    assert response.json["status"] == "false"
    assert response.status_code == 400


def test_registration_fail_invalid_password(client, db, user):
    register_data = {"name": "abc", "email": "abc@gmail.com", "password": "abc", "user_type_id": 1}
    response = client.post("/registration", data=json.dumps(register_data), content_type="application/json")
    assert response.json["message"] == "Please enter proper password"
    assert response.json["status"] == "false"
    assert response.status_code == 400


def test_registration_fail_invalid_data(client, db, user):
    register_data = {"nameee": "abc", "emailll": "abc@gmail.com", "passworddd": "Abc@123", "user_type_iddd": 1}
    response = client.post("/registration", data=json.dumps(register_data), content_type="application/json")
    assert response.json["message"] == "Please enter proper data"
    assert response.json["status"] == "false"
    assert response.status_code == 400


def test_get_profile(client, db, user):
    access_token = test_login_success(client, db, user)
    response = client.get("/profile", headers={"Authorization": access_token})
    assert response.json["message"] == "user data fetched successfully"
    assert response.json["status"] == "true"
    assert response.status_code == 200


def test_update_profile_success(client, db, user):
    access_token = test_login_success(client, db, user)
    update_profile_data = {"name": "Adminnn", "email": "admin@gmail.com"}
    response = client.put("/update_profile", headers={"Authorization": access_token},
                          data=json.dumps(update_profile_data), content_type="application/json")
    assert response.json["message"] == "Profile Updated Successfully"
    assert response.json["status"] == "true"
    assert response.status_code == 200


def test_update_profile_invalid_data(client, db, user):
    access_token = test_login_success(client, db, user)
    update_profile_data = {"nameee": "Admin", "emailll": "admin@gmail.com"}
    response = client.put("/update_profile", headers={"Authorization": access_token},
                          data=json.dumps(update_profile_data), content_type="application/json")
    assert response.json["message"] == "Please enter proper data"
    assert response.json["status"] == "false"
    assert response.status_code == 400


def test_update_profile_invalid_email(client, db, user):
    access_token = test_login_success(client, db, user)
    update_profile_data = {"name": "Admin", "email": "@gmail.com"}
    response = client.put("/update_profile", headers={"Authorization": access_token},
                          data=json.dumps(update_profile_data), content_type="application/json")
    assert response.json["message"] == "Please enter proper email"
    assert response.json["status"] == "false"
    assert response.status_code == 400


def test_update_profile_invalid_name(client, db, user):
    access_token = test_login_success(client, db, user)
    update_profile_data = {"name": "Admin123", "email": "admin@gmail.com"}
    response = client.put("/update_profile", headers={"Authorization": access_token},
                          data=json.dumps(update_profile_data), content_type="application/json")
    assert response.json["message"] == "Please enter proper name"
    assert response.json["status"] == "false"
    assert response.status_code == 400


def test_update_profile_email_already_exists(client, db, user):
    access_token = test_login_success(client, db, user)
    update_profile_data = {"name": "Admin", "email": "user@gmail.com"}
    response = client.put("/update_profile", headers={"Authorization": access_token},
                          data=json.dumps(update_profile_data), content_type="application/json")
    assert response.json["message"] == "user with this email id already exists please choose different email"
    assert response.json["status"] == "false"
    assert response.status_code == 400


def test_change_password_success(client, db, user):
    access_token = test_login_success(client, db, user)
    change_password_data = {"current_password": "abc", "new_password": "Abc@123"}
    response = client.post("/change_password", headers={"Authorization": access_token},
                           data=json.dumps(change_password_data), content_type="application/json")
    assert response.json["message"] == "Password changed successfully"
    assert response.json["status"] == "true"
    assert response.status_code == 200


def test_change_password_fail_proper_password(client, db, user):
    access_token = test_login_success(client, db, user)
    change_password_data = {"current_password": "abc", "new_password": "123"}
    response = client.post("/change_password", headers={"Authorization": access_token},
                           data=json.dumps(change_password_data), content_type="application/json")
    assert response.json["message"] == "Please enter proper password"
    assert response.json["status"] == "false"
    assert response.status_code == 400


def test_change_password_fail_invalid_current_password(client, db, user):
    access_token = test_login_success(client, db, user)
    change_password_data = {"current_password": "123", "new_password": "Abc@123"}
    response = client.post("/change_password", headers={"Authorization": access_token},
                           data=json.dumps(change_password_data), content_type="application/json")
    assert response.json["message"] == "Invalid current password"
    assert response.json["status"] == "false"
    assert response.status_code == 400


def test_change_password_fail_invalid_data(client, db, user):
    access_token = test_login_success(client, db, user)
    change_password_data = {"current_passworddd": "abc", "new_passworddd": "Abc@123"}
    response = client.post("/change_password", headers={"Authorization": access_token},
                           data=json.dumps(change_password_data), content_type="application/json")
    assert response.json["message"] == "Please enter proper data"
    assert response.json["status"] == "false"
    assert response.status_code == 400


def test_get_show_articles(client, db, user):
    response = client.get("/show_articles")
    assert response.json["message"] == "Articles fetched successfully"
    assert response.json["status"] == "true"
    assert response.status_code == 200


def test_reset_password_request_success(client, db, user):
    reset_password_request_data = {"email": "admin@gmail.com"}
    response = client.post("/reset_password_request",
                           data=json.dumps(reset_password_request_data), content_type="application/json")
    assert response.json["message"] == "An email has been sent to your id please check it to reset your password."
    assert response.json["status"] == "true"
    assert response.status_code == 200
    return response.json["data"]


def test_reset_password_request_invalid_email(client, db, user):
    access_token = test_login_success(client, db, user)
    reset_password_request_data = {"email": "hey@gmail.com"}
    response = client.post("/reset_password_request", headers={"Authorization": access_token},
                           data=json.dumps(reset_password_request_data), content_type="application/json")
    assert response.json["message"] == "Invalid email id. Please enter valid email."
    assert response.json["status"] == "false"
    assert response.status_code == 404


def test_reset_password_request_invalid_data(client, db, user):
    access_token = test_login_success(client, db, user)
    reset_password_request_data = {"emailll": "admin@gmail.com"}
    response = client.post("/reset_password_request", headers={"Authorization": access_token},
                           data=json.dumps(reset_password_request_data), content_type="application/json")
    assert response.json["message"] == "Enter proper data"
    assert response.json["status"] == "false"
    assert response.status_code == 400


def test_reset_password_valid_token(client, db, user):
    reset_password_token = test_reset_password_request_success(client, db, user)
    reset_password_data = {"token": reset_password_token, "password": "Abc@123"}
    response = client.post("/reset_password",
                           data=json.dumps(reset_password_data), content_type="application/json")
    assert response.json["message"] == "Your password has been updated! You can now log in"
    assert response.json["status"] == "true"
    assert response.status_code == 200


def test_reset_password_invalid_token(client, db, user):
    reset_password_token = test_reset_password_request_success(client, db, user)
    reset_password_data = {"token": f"{reset_password_token}abc", "password": "Abc@123"}
    response = client.post("/reset_password",
                           data=json.dumps(reset_password_data), content_type="application/json")
    assert response.json["message"] == "That is an invalid or expired token"
    assert response.json["status"] == "false"
    assert response.status_code == 400


def test_reset_password_invalid_password(client, db, user):
    reset_password_token = test_reset_password_request_success(client, db, user)
    reset_password_data = {"token": reset_password_token, "password": "123"}
    response = client.post("/reset_password",
                           data=json.dumps(reset_password_data), content_type="application/json")
    assert response.json["message"] == "Please enter proper password"
    assert response.json["status"] == "false"
    assert response.status_code == 400


def test_reset_password_invalid_data(client, db, user):
    reset_password_token = test_reset_password_request_success(client, db, user)
    reset_password_data = {"tokennn": reset_password_token, "passworddd": "Abc@123"}
    response = client.post("/reset_password",
                           data=json.dumps(reset_password_data), content_type="application/json")
    assert response.json["message"] == "Enter proper data"
    assert response.json["status"] == "false"
    assert response.status_code == 400
