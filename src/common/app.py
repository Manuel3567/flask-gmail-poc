from flask import Flask, session, render_template_string, redirect, url_for
from . import oauth
import os
from .google import google
from dotenv import load_dotenv

load_dotenv()
CLIENT_ID = os.environ.get("CLIENT_ID")
CLIENT_SECRET = os.environ.get("CLIENT_SECRET")
FLASK_SESSION_KEY = os.environ.get("FLASK_SESSION_KEY")


MAIL_SCOPE = "https://mail.google.com/"

app = Flask(__name__)
app.secret_key = FLASK_SESSION_KEY

oauth.init_app(app)
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
  <button type="submit" formaction="{{ url_for("google.mail") }}">Send mail</button>
</form>
{% else %}
<form method="get">
  <button type="submit" formaction="{{ url_for("google.authorize") }}">Go to Google</button>
</form>

{% endif %}
<form method="post">
  <button type="submit" formaction="{{ url_for(".logout") }}">Logout</button>
</form>
"""

app.register_blueprint(google, url_prefix="/google")


@app.route("/")
def index():
    token = session.get("token")

    return render_template_string(INDEX, token=token)


@app.post("/logout")
def logout():
    session.clear()  # removes all session data
    return redirect(url_for("index"))
