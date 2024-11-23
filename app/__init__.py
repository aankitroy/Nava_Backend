import os
import random
import string
from app.utils.database import master_db, save_master_db
from app.utils.config import settings

def create_super_admin():
    if "users" not in master_db:
        master_db["users"] = []
    
    if not any(user.get("role") == "super_admin" for user in master_db["users"]):
        super_admin_password = settings.SUPER_ADMIN_PASSWORD
        master_db["users"].append({
            "email": "super_admin@gmail.com",
            "password": super_admin_password,
            "role": "super_admin"
        })
        save_master_db(master_db)
        print(f"Super admin created with username 'super_admin' and password '{super_admin_password}'")

def create_admin_via_super_admin(super_admin_email: str, admin_email: str):
    if any(user.get("email") == super_admin_email and user.get("role") == "super_admin" for user in master_db["users"]):
        if not any(user.get("email") == admin_email for user in master_db["users"]):
            admin_password = settings.FIRST_ADMIN_PASSWORD
            master_db["users"].append({
                "email": admin_email,
                "password": admin_password,
                "role": "admin"
            })
            save_master_db(master_db)
            print(f"Admin created with email '{admin_email}' and password '{admin_password}'")
    else:
        print("Super admin authentication failed. Cannot create admin.")

create_super_admin()
create_admin_via_super_admin("super_admin@gmail.com", "first_admin@gmail.com")