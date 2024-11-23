import pytest
from fastapi.testclient import TestClient
from app.api_v1.org.service import router
from app.utils.database import master_db, save_master_db
from app.api_v1.user.service import create_access_token
from datetime import timedelta
from fastapi import HTTPException

# Create a TestClient instance
client = TestClient(router)

# Sample data
admin_email = "super_admin@gmail.com"
admin_token = create_access_token(data={"sub": admin_email}, expires_delta=timedelta(minutes=15))

@pytest.fixture(autouse=True)
def setup_and_teardown():
    # Setup: Store the initial state of master_db
    initial_master_db_state = master_db.copy()
    yield
    # Teardown: Restore the initial state of master_db
    master_db.clear()
    master_db.update(initial_master_db_state)
    save_master_db(master_db)

def test_create_organization_success():
    headers = {"Authorization": f"Bearer {admin_token}"}
    response = client.post("/create", json={"organization_name": "TestOrg", "email": admin_email}, headers=headers)
    assert response.status_code == 200
    assert response.json() == {"message": "Organization created successfully", "organization_name": "TestOrg"}

def test_create_organization_already_exists():
    headers = {"Authorization": f"Bearer {admin_token}"}
    # Create the organization first
    client.post("/create", json={"organization_name": "TestOrg", "email": admin_email}, headers=headers)
    # Try to create the same organization again
    with pytest.raises(HTTPException) as exc_info:
        response = client.post("/create", json={"organization_name": "TestOrg", "email": admin_email}, headers=headers)

    assert exc_info.value.status_code == 400
    assert exc_info.value.detail == "Organization already exists"

def test_get_organization_success():
    headers = {"Authorization": f"Bearer {admin_token}"}
    # Create the organization first
    client.post("/create", json={"organization_name": "TestOrg", "email": admin_email}, headers=headers)
    # Retrieve the organization
    response = client.get("/get", params={"organization_name": "TestOrg"}, headers=headers)
    assert response.status_code == 200
    assert response.json() == {"organization_name": "TestOrg"}

def test_get_organization_not_found():
    headers = {"Authorization": f"Bearer {admin_token}"}
    with pytest.raises(HTTPException) as exc_info:
        response = client.get("/get", params={"organization_name": "NonExistentOrg"}, headers=headers)
    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Organization not found"

def test_get_organization_access_forbidden():
    headers = {"Authorization": f"Bearer {admin_token}"}
    # Create the organization with a different admin email
    
    client.post("/create", json={"organization_name": "TestOrg", "email": "super_admin@gmail.com"}, headers=headers)
    # Try to access the organization with a different admin
    another_admin_token = create_access_token(data={"sub": "new_admin@example.com"}, expires_delta=timedelta(minutes=15))
    headers = {"Authorization": f"Bearer {another_admin_token}"}

    with pytest.raises(HTTPException) as exc_info:
        response = client.get("/get", params={"organization_name": "TestOrg"}, headers=headers)
    assert exc_info.value.status_code == 403
    assert exc_info.value.detail == "Access forbidden: You are not the admin of this organization"