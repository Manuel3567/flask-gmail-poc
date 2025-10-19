from flask import Flask, session
from authlib.integrations.flask_client import OAuth
from flask import url_for, redirect, render_template_string
import base64
from email.mime.text import MIMEText
import os

CLIENT_ID = os.environ.get("CLIENT_ID")
CLIENT_SECRET = os.environ.get("CLIENT_SECRET")
FLASK_SESSION_KEY = os.environ.get("FLASK_SESSION_KEY")


MAIL_SCOPE = "https://mail.google.com/"

app = Flask(__name__)
app.secret_key = FLASK_SESSION_KEY

oauth = OAuth(app)
oauth.register(
    "google",
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    authorize_url="https://accounts.google.com/o/oauth2/auth",
    access_token_url="https://oauth2.googleapis.com/token",
    api_base_url="https://gmail.googleapis.com/",
    client_kwargs={"scope": f"openid profile email {MAIL_SCOPE}"},
)

INDEX = """
{% if token %}
<p>hello {{ token["userinfo"]["email"] }} </p>
<form method="post">
  <button type="submit" formaction="/google/mail">Send mail</button>
</form>
{% else %}
<form method="get">
  <button type="submit" formaction="/google/authorize">Go to Google</button>
</form>

{% endif %}
"""


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


@app.route("/")
def index():
    token = session.get("token")

    return render_template_string(INDEX, token=token)


@app.post("/google/mail")
def mail():
    token = session.get("token")
    if token:
        response = send_mail(token)
        print(response)
    return redirect("/")


@app.route("/google/token")
def google_token():
    token = oauth.google.authorize_access_token()
    session["token"] = token
    return redirect("/")


@app.route("/google/authorize")
def google_authorize():
    redirect_uri = url_for("google_token", _external=True)
    return oauth.google.authorize_redirect(redirect_uri)
