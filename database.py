# database.py 
import json
import os

DB_FILE = "user_db.json"

def save_user_data(user_id, data):
    all_data = {}
    if os.path.exists(DB_FILE):
        with open(DB_FILE, 'r') as f:
            try:
                all_data = json.load(f)
            except json.JSONDecodeError:
                pass
    all_data[user_id] = data
    with open(DB_FILE, 'w') as f:
        json.dump(all_data, f, indent=4)
    print(f"\n[DB Log] Data saved for user '{user_id}'.")

def load_user_data(user_id):
    if not os.path.exists(DB_FILE):
        return None
    with open(DB_FILE, 'r') as f:
        try:
            all_data = json.load(f)
            return all_data.get(user_id)
        except json.JSONDecodeError:
            return None