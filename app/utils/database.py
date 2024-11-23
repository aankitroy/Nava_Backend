from typing import Dict
import json
import os

# Define the path to the JSON file
db_file_path = "master_db.json"

# Check if the JSON file exists
if os.path.exists(db_file_path):
    # Load the database from the JSON file
    with open(db_file_path, "r") as db_file:
        master_db: Dict[str, Dict] = json.load(db_file)
else:
    # Create an empty database and save it to the JSON file
    master_db: Dict[str, Dict] = {}
    with open(db_file_path, "w") as db_file:
        json.dump(master_db, db_file)

def save_master_db(master_db: Dict[str, Dict]):
    with open(db_file_path, "w") as db_file:
        json.dump(master_db, db_file)

def create_dynamic_org_db(org_name: str):
    org_db_file_path = f"{org_name}.json"
    if not os.path.exists(org_db_file_path):
        with open(org_db_file_path, "w") as org_db_file:
            json.dump({}, org_db_file)
