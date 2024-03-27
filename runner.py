import requests
import functions_framework
import sqlalchemy
import os
from datetime import datetime

DB_USER = os.environ.get('DB_USER')
DB_PASSWORD = os.environ.get('DB_PASSWORD')
DB_HOST = os.environ.get('DB_HOST')
DB_NAME = os.environ.get('DB_NAME')

db_connection = sqlalchemy.create_engine(f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:5432/{DB_NAME}")

def mailgun_caller(email, name, token):
    return requests.post(
        "https://api.mailgun.net/v3/csye6225-assignment.store/messages",
        auth=("api", "f2767b81d6c08b78f6add8d5b0db6e2e-f68a26c9-fd791041"),
        data={"from": "Webapp Sender <mailgun@csye6225-assignment.store>",
            "to": email,
            "subject": "Verify your account",
            "template": "csye6225-template",
            "h:X-Mailgun-Variables": {
                "name": name,
                "verification_url": "http://csye6225-assignment.store:8000/v1/user/verify?token="+token
                }
            }
        )

@functions_framework.cloud_event
def runner_func(request):
    request_obj = request.get_json()
    user_id = request_obj['id']
    name = request_obj['firstname']+ " " +request_obj['lastname']
    email = request_obj['email']
    token = request_obj['token']

    mailgun_caller(email, name, token)
    db_connection.execute(f"INSERT INTO user_auth_useremailverificationtrack (user_id, token, created_at) VALUES ('{user_id}', '{token}', '{datetime.now()})")
    return 'Mail sent successfully'
