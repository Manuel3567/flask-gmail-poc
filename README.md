# Flask Gmail API Example

This is a simple Flask application demonstrating how to authenticate with Google OAuth2 and send an email using the Gmail API.

## Features

-   Google OAuth2 login
-   Send an email to the logged-in user's Gmail account
-   Uses `Authlib` for OAuth2 integration

## Prerequisites

-   Python 3.12+
-   A Google Cloud project with OAuth 2.0 Client ID and Client Secret
-   Flask, Authlib installed

## Setup
Create a `.env` file with the following values:
```
export CLIENT_ID="your-google-client-id"
export CLIENT_SECRET="your-google-client-secret"
export FLASK_SESSION_KEY="a-random-secret-key"
```

The client id and secret can be obtained from the google authorization server:
https://console.cloud.google.com/auth/clients