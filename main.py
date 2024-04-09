import requests
from cloudevents.http import CloudEvent
import json
import base64
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
    link_to_verify = f"https://csye6225-assignment.store/v1/user/verify?token={token}"
    return requests.post(
        "https://api.mailgun.net/v3/csye6225-assignment.store/messages",
        auth=("api", "f2767b81d6c08b78f6add8d5b0db6e2e-f68a26c9-fd791041"),
        data={"from": "Webapp Sender <mailgun@csye6225-assignment.store>",
            "to": email,
            "subject": "Verify your account",
            "html": f"""
            <html>
            <body>
            <h3>Hi {name},</h3>
            <p>Click the link below to verify your account</p>
            <a href="{link_to_verify}">{link_to_verify}</a>
            <p>Thanks</p>
            <p>Webapp</p>
            </body>
            </html
            """
            }
        )


@functions_framework.cloud_event
def runner_func(cloud_event: CloudEvent):
    request_obj = json.loads(base64.b64decode(cloud_event.data["message"]["data"]).decode())
    user_id = request_obj["id"]
    name = request_obj["firstname"] + " " + request_obj["lastname"]
    email = request_obj["email"]
    token = request_obj["token"]

    mailgun_caller(email, name, token)

    query = f"""UPDATE user_auth_user SET email_token_generated = '{token}', email_token_generated_at = '{datetime.now()}' WHERE id = '{user_id}'"""
    with db_connection.connect() as connection:
        connection.execute(query)
    return 'Mail sent successfully'
