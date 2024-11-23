from app.api_v1.user.schema import LoginRequest
from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta
from jose import JWTError, jwt
from app.utils.config import settings
from app.api_v1.user.schema import AdminCreateRequest
from app.utils.database import master_db, save_master_db
from fastapi.security import OAuth2PasswordRequestForm
from app.api_v1.user.schema import AdminDeleteRequest

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/v1/user/login", scheme_name="JWT")

def validate_token_for_admin(token: str = Depends(oauth2_scheme)) -> str:
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.ALGORITHM])
        email = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        
        # Check if the email belongs to an admin in the user table/collection in master_db
        if "users" in master_db:
            for user in master_db["users"]:
                if user["email"] == email and (user["role"] == "admin" or user["role"] == "super_admin"):
                    return email
        
        raise HTTPException(status_code=403, detail="Only admin can access this resource")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

def validate_token_for_super_admin(token: str = Depends(oauth2_scheme)) -> str:
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.ALGORITHM])
        email = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        
        # Check if the email belongs to a super admin in the user table/collection in master_db
        if "users" in master_db:
            for user in master_db["users"]:
                if user["email"] == email and user["role"] == "super_admin":
                    return email
        
        raise HTTPException(status_code=403, detail="Only super admin can access this resource")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")


def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

@router.post("/login")
def admin_login(form_data: OAuth2PasswordRequestForm = Depends()):
    if "users" in master_db:
        for user in master_db["users"]:
            if user["email"] == form_data.username and user["password"] == form_data.password and (user["role"] == "admin" or user["role"] == "super_admin"):
                access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
                access_token = create_access_token(
                    data={"sub": form_data.username}, expires_delta=access_token_expires
                )
                return {"access_token": access_token, "token_type": "bearer"}
    raise HTTPException(status_code=401, detail="Invalid credentials")


@router.post("/create-admin")
def create_admin(request: AdminCreateRequest, super_admin_email: str = Depends(validate_token_for_super_admin)):
    # Check if the admin already exists
    if "users" not in master_db:
        master_db["users"] = []

    for user in master_db["users"]:
        if user["email"] == request.email:
            raise HTTPException(status_code=400, detail="Admin already exists")

    # Create a new admin in the user table/collection in the master database
    master_db["users"].append({
        "email": request.email,
        "password": request.password,
        "role": "admin"
    })

    save_master_db(master_db)

    return {"message": "Admin created successfully", "email": request.email}


@router.delete("/delete-admin")
def delete_admin(email: str, super_admin_email: str = Depends(validate_token_for_super_admin)):
    # Check if the admin exists
    if "users" not in master_db:
        raise HTTPException(status_code=404, detail="Admin not found")

    for user in master_db["users"]:
        if user["email"] == email and user["role"] == "admin":
            master_db["users"].remove(user)
            save_master_db(master_db)
            return {"message": "Admin deleted successfully", "email": email}

    raise HTTPException(status_code=404, detail="Admin not found")