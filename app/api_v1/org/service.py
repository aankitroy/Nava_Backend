from fastapi import APIRouter, HTTPException, Depends
from typing import Dict
from app.api_v1.org.schema import OrganizationCreateRequest
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from datetime import datetime, timedelta
from app.utils.config import settings
from app.api_v1.user.service import validate_token_for_admin
from app.utils.database import master_db
import uuid
from app.utils.database import save_master_db, create_dynamic_org_db


router = APIRouter()

@router.post("/create")
def create_organization(request: OrganizationCreateRequest, email: str = Depends(validate_token_for_admin)):

    # Check if the organization already exists in the master database
    if "org_database" in master_db:
        for org_id, org_data in master_db["org_database"].items():
            if org_data["org_name"] == request.organization_name:
                raise HTTPException(status_code=400, detail="Organization already exists")

    # Create a dynamic DB for the organization
    org_db = {
        "admin": {
            "email": email, #password is not required for admin here, it is only required for user collection
        },
        "org_name": request.organization_name,
        "database": "org_"+request.organization_name
    }

    # Store the dynamic DB information in the master database
    unique_id = str(uuid.uuid4())
    if "org_database" not in master_db:
        master_db["org_database"] = {}
    master_db["org_database"][unique_id] = org_db

    save_master_db(master_db)
    create_dynamic_org_db("org_"+unique_id)

    return {"message": "Organization created successfully", "organization_name": request.organization_name}


@router.get("/get")
def get_organization(organization_name: str, email: str = Depends(validate_token_for_admin)):
    if "org_database" not in master_db:
        raise HTTPException(status_code=404, detail="Organization not found")

    organization = None
    for org_id, org_data in master_db["org_database"].items():
        if org_data["org_name"] == organization_name:
            organization = org_data
            break

    if organization is None:
        raise HTTPException(status_code=404, detail="Organization not found")

    if organization['admin']['email'] != email:
        raise HTTPException(status_code=403, detail="Access forbidden: You are not the admin of this organization")

    return {"organization_name": organization["org_name"]}
