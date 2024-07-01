from app import create_app
from database.models import user_datastore

app, api = create_app()

def generate_sample_token():
    tokens = {"Admin": "", "Manager": "", "Customer": ""}
    admin_user = user_datastore.find_user(email='admin@a.com')
    manager_user = user_datastore.find_user(email='manager@a.com')
    customer_user = user_datastore.find_user(email='customer@a.com')

    if admin_user:
        tokens["Admin"] = admin_user.get_auth_token()

    if manager_user:
        tokens["Manager"] = manager_user.get_auth_token()
    
    if customer_user:
        tokens["Customer"] = customer_user.get_auth_token()
    
    return tokens

with app.app_context():
    tokens = generate_sample_token()
    with open('tokens.txt', 'w') as file:
        for role, token in tokens.items():
            file.write(f"{role} token: {token}\n")