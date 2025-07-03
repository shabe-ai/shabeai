def test_auth_register_success(client):
    """Test successful user registration"""
    response = client.post(
        "/auth/register",
        json={
            "email": "newuser@example.com",
            "password": "testpass123",
            "full_name": "Test User",
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "newuser@example.com"
    assert data["full_name"] == "Test User"
    assert "id" in data


def test_auth_register_invalid_password(client):
    """Test registration with invalid password (too short)"""
    response = client.post(
        "/auth/register",
        json={
            "email": "test@example.com",
            "password": "123",  # too short
            "full_name": "Test User",
        },
    )
    assert response.status_code == 400


def test_auth_login_success(client):
    """Test successful login"""
    # First register a user
    client.post(
        "/auth/register",
        json={
            "email": "login@example.com",
            "password": "testpass123",
            "full_name": "Login User",
        },
    )

    # Then login
    response = client.post(
        "/auth/jwt/login",
        data={"username": "login@example.com", "password": "testpass123"},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    assert response.status_code == 204
    assert "crm-auth" in response.cookies


def test_auth_login_invalid_credentials(client):
    """Test login with invalid credentials"""
    response = client.post(
        "/auth/jwt/login",
        data={"username": "nonexistent@example.com", "password": "wrongpass"},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    assert response.status_code == 400


def test_auth_me_endpoint(client):
    """Test /users/me endpoint with valid authentication"""
    # Register and login
    client.post(
        "/auth/register",
        json={
            "email": "me@example.com",
            "password": "testpass123",
            "full_name": "Me User",
        },
    )

    login_response = client.post(
        "/auth/jwt/login",
        data={"username": "me@example.com", "password": "testpass123"},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    cookie = login_response.cookies.get("crm-auth")

    # Test /users/me
    response = client.get("/users/me", cookies={"crm-auth": cookie})
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "me@example.com"


def test_auth_me_unauthorized(client):
    """Test /users/me endpoint without authentication"""
    response = client.get("/users/me")
    assert response.status_code == 401


def test_auth_logout(client):
    """Test logout functionality"""
    # Register and login first
    client.post(
        "/auth/register",
        json={
            "email": "logout@example.com",
            "password": "testpass123",
            "full_name": "Logout User",
        },
    )

    login_response = client.post(
        "/auth/jwt/login",
        data={"username": "logout@example.com", "password": "testpass123"},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    cookie = login_response.cookies.get("crm-auth")

    # Test logout
    response = client.post("/auth/jwt/logout", cookies={"crm-auth": cookie})
    assert response.status_code == 204
