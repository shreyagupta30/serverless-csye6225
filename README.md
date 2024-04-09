# Serverless Microservice

Python Cloud Function for Email Verification
This repository contains a Python script that is designed to be deployed as a Cloud Function. The function listens for CloudEvents, specifically for events that indicate a new user has registered. Upon receiving such an event, the function sends an email to the new user for account verification.

## Functionality
The main functionality of this script is contained within the `runner_func` function. This function is triggered by a CloudEvent. It decodes the event data to retrieve the user's information, including their ID, name, email, and a token. It then calls the mailgun_caller function to send an email to the user with a verification link.

The `mailgun_caller` function sends an HTTP POST request to the Mailgun API to send the email. The email contains a link for the user to verify their account.

After the email is sent, the runner_func function updates the `user_auth_user` table in a PostgreSQL database to indicate that an email token has been generated for the user.

## Environment Variables
The script uses the following environment variables:

`DB_USER`: The username for the PostgreSQL database.
`DB_PASSWORD`: The password for the PostgreSQL database.
`DB_HOST`: The host of the PostgreSQL database.
`DB_NAME`: The name of the PostgreSQL database.

## Dependencies
The script depends on the following Python libraries:

`requests`: For making HTTP requests to the Mailgun API.
cloudevents: For handling CloudEvents.
`json`: For parsing JSON data.
`base64`: For decoding base64-encoded data.
`functions_framework`: For defining the Cloud Function.
`sqlalchemy`: For interacting with the PostgreSQL database.
`os`: For accessing environment variables.
`datetime`: For getting the current date and time.
