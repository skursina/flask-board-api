def test_register(client):

    response = client.post(
        "/register",
        json={
            "email": "test@test.com",
            "password": "123456"
        }
    )

    assert response.status_code == 201

    data = response.get_json()

    assert data["message"] == "user created"


def test_login(client):

    client.post(
        "/register",
        json={
            "email": "test@test.com",
            "password": "123456"
        }
    )


    response = client.post(
        "/login",
        json={
            "email": "test@test.com",
            "password": "123456"
        }
    )


    assert response.status_code == 200


    data = response.get_json()

    assert "access_token" in data


def get_token(client):

    client.post(
        "/register",
        json={
            "email":"test@test.com",
            "password":"123456"
        }
    )


    response = client.post(
        "/login",
        json={
            "email":"test@test.com",
            "password":"123456"
        }
    )

    return response.get_json()["access_token"]



def test_create_ad(client):

    token = get_token(client)


    response = client.post(
        "/ads",
        json={
            "title":"Ноутбук",
            "description":"RTX 4060"
        },
        headers={
            "Authorization": f"Bearer {token}"
        }
    )


    assert response.status_code == 201


def test_get_ad(client):

    token = get_token(client)


    client.post(
        "/ads",
        json={
            "title":"Ноутбук",
            "description":"RTX 4060"
        },
        headers={
            "Authorization": f"Bearer {token}"
        }
    )


    response = client.get("/ads/1")


    assert response.status_code == 200


    data=response.get_json()

    assert data["title"] == "Ноутбук"


def test_create_ad_without_token(client):

    response = client.post(
        "/ads",
        json={
            "title": "Ноутбук",
            "description": "RTX 4060"
        }
    )

    assert response.status_code == 401


def test_user_cannot_delete_foreign_ad(client):

    # создаём первого пользователя
    token1 = get_token(client)


    client.post(
        "/ads",
        json={
            "title": "Ноутбук",
            "description": "RTX"
        },
        headers={
            "Authorization": f"Bearer {token1}"
        }
    )


    # создаём второго пользователя
    client.post(
        "/register",
        json={
            "email": "user2@test.com",
            "password": "123456"
        }
    )


    login = client.post(
        "/login",
        json={
            "email": "user2@test.com",
            "password": "123456"
        }
    )


    token2 = login.get_json()["access_token"]


    response = client.delete(
        "/ads/1",
        headers={
            "Authorization": f"Bearer {token2}"
        }
    )


    assert response.status_code == 403