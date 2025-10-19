from flask import session, redirect, url_for, Blueprint
from email.mime.text import MIMEText
import base64
from . import oauth

google = Blueprint("google", __name__)


def send_mail(token):
    email = token["userinfo"]["email"]
    message = MIMEText("This is a test email sent from Flask using Gmail REST API!")
    message["to"] = email
    message["from"] = "me"
    message["subject"] = "Hello from Gmail API"

    # Gmail expects base64url encoding (not standard base64)
    raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode("utf-8")

    resp = oauth.google.post(
        "gmail/v1/users/me/messages/send", token=token, json={"raw": raw_message}
    )

    if resp.status_code == 200:
        return f"<p>Email sent!</p><pre>{resp.json()}</pre>"
    else:
        return f"<p>Failed: {resp.status_code}</p><pre>{resp.text}</pre>"


@google.post("/mail")
def mail():
    token = session.get("token")
    if token:
        response = send_mail(token)
        print(response)
    return redirect("/")


@google.route("/authorize")
def authorize():
    redirect_uri = url_for("google.get_token", _external=True)
    return oauth.google.authorize_redirect(redirect_uri)


@google.route("/token")
def get_token():
    token = oauth.google.authorize_access_token()
    session["token"] = token
    return redirect("/")
