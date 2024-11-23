import pytest
from fastapi.testclient import TestClient
from app.api_v1.user.service import router, create_access_token
from app.utils.database import master_db, save_master_db
from app.utils.config import settings
from datetime import timedelta
from fastapi import HTTPException
# Create a TestClient instance
client = TestClient(router)

# Sample user data
admin_user = {
    "email": "admin@example.com",
    "password": "adminpass",
    "role": "admin"
}

@pytest.fixture(autouse=True)
def setup_and_teardown():
    # Setup: Store the initial state of master_db
    initial_master_db_state = master_db.copy()
    yield
    # Teardown: Restore the initial state of master_db
    master_db.clear()
    master_db.update(initial_master_db_state)
    save_master_db(master_db)

def test_admin_login_success():
    response = client.post(
        "/login",
        data={"username": "super_admin@gmail.com", "password": "q~S$H7e;i\"vC"}
    )
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_admin_login_failure():
    with pytest.raises(HTTPException) as exc_info:
        response = client.post("/login", data={"username": "admin@example.com", "password": "wrongpass"})
    assert exc_info.value.status_code == 401
    assert exc_info.value.detail == "Invalid credentials"

def test_create_admin_success():
    # Create a valid token for the admin user
    token = create_access_token(data={"sub": "super_admin@gmail.com"}, expires_delta=timedelta(minutes=15))
    headers = {"Authorization": f"Bearer {token}"}

    response = client.post("/create-admin", json={"email": "newadmin@example.com", "password": "newadminpass"}, headers=headers)
    assert response.status_code == 200
    assert response.json() == {"message": "Admin created successfully", "email": "newadmin@example.com"}

    response = client.delete(
        "/delete-admin",
        params={"email": "newadmin@example.com"},
        headers=headers
    )
    assert response.status_code == 200
    assert response.json() == {"message": "Admin deleted successfully", "email": "newadmin@example.com"}

    

def test_create_admin_failure_existing_user():
    # Create a valid token for the admin user
    token = create_access_token(data={"sub": "super_admin@gmail.com"}, expires_delta=timedelta(minutes=15))
    headers = {"Authorization": f"Bearer {token}"}

    # Attempt to create an admin with an existing email
    with pytest.raises(HTTPException) as exc_info:
        response = client.post("/create-admin", json={"email": "super_admin@gmail.com", "password": "adminpass"}, headers=headers)
    assert exc_info.value.status_code == 400
    assert exc_info.value.detail == "Admin already exists"

def test_create_admin_failure_invalid_token():
    headers = {"Authorization": "Bearer invalidtoken"}

    with pytest.raises(HTTPException) as exc_info:
        response = client.post("/create-admin", json={"email": "newadmin@example.com", "password": "newadminpass"}, headers=headers)
    assert exc_info.value.status_code == 401
    assert exc_info.value.detail == "Invalid token"