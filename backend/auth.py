import json
import hashlib

def load_admin():
    with open('data/admin.json', 'r') as f:
        return json.load(f)

def check_login(username, password):
    admin = load_admin()
    return (
        username == admin['username'] and
        password == admin['password']
    )