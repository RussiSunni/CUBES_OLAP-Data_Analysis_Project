# Python standard libraries
import json
import os
import sqlite3

# Third party libraries
from flask import Flask, redirect, request, url_for, render_template
from flask_login import (
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user
)

from oauthlib.oauth2 import WebApplicationClient
import requests

# Internal imports
from db import init_db_command
from user import User

# Cubes imports
from cubes.server import slicer
from cubes.compat import ConfigParser


# Cubes settings
settings = ConfigParser()
settings.read("../Cubes/cubes-master/examples/hello_world/slicer.ini")

# Google OAuth details - do not commit to Github, keep secret ------------------------------------
GOOGLE_CLIENT_ID = ''
GOOGLE_CLIENT_SECRET = ''
GOOGLE_DISCOVERY_URL = (
    "https://accounts.google.com/.well-known/openid-configuration"
)

# Flask app setup
app = Flask(__name__, template_folder='../Cubes/cubesviewer/html', static_folder='../Cubes/cubesviewer')
app.secret_key = os.environ.get("SECRET_KEY") or os.urandom(24)


# User session management setup
# https://flask-login.readthedocs.io/en/latest
login_manager = LoginManager()
login_manager.init_app(app)



# implement roles, extend Flask-login

from functools import wraps

def login_required(role="FIN"):
    def wrapper(fn):
        @wraps(fn)
        def decorated_view(*args, **kwargs):
            if not current_user.is_authenticated:
                return login_manager.unauthorized()
            if ((current_user.role != role) and (role != "ANY")):
                return login_manager.unauthorized()
            return fn(*args, **kwargs)
        return decorated_view
    return wrapper


@login_manager.unauthorized_handler
def unauthorized():
    return "You must be logged in to access this content.", 403


# Naive database setup
try:
    init_db_command()
except sqlite3.OperationalError:
     # Assume it's already been created
    pass

# --------------------------------------


# OAuth2 client setup
client = WebApplicationClient(GOOGLE_CLIENT_ID)

# Flask-Login helper to retrieve a user from our db
@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)


# routes --------------------------

@app.route("/")
def index():
    if current_user.is_authenticated:
        role = current_user.role
        return render_template('index.html', value = role)

    else:
        return 'Please login with your Construct <a class="button" href="/log-in">Google Login</a>'



# I think these 2 lines need to be here, below the root route -----------------
app.config["DEBUG"] = True
app.register_blueprint(slicer, config=settings)

# -----------------------------------------------------------------------------


@app.route('/tutorial')
@login_required(role="ANY")
def tutorial():
     return render_template('tutorial.html')

@app.route('/viewer')
@login_required(role="ANY")
def viewer():
     return render_template('studio.html')

@app.route('/teams_hours')
@login_required(role="ANY")
def teams_hours():
    return render_template('teams_hours.html')

@app.route('/non_billable_analysis')
@login_required(role="ANY")
def non_billable_analysis():
    return render_template('non_billable_analysis.html')

@app.route('/total')
@login_required(role="ANY")
def total():
    return render_template('total.html')

@app.route('/test')
@login_required(role="FIN")
def test():
    return 'you have the correct role for this page'


@app.route("/log-in")
def login():
    # Find out what URL to hit for Google login
    google_provider_cfg = get_google_provider_cfg()
    authorization_endpoint = google_provider_cfg["authorization_endpoint"]

    # Use library to construct the request for login and provide
    # scopes that let you retrieve user's profile from Google
    request_uri = client.prepare_request_uri(
        authorization_endpoint,
        redirect_uri=request.base_url + "/callback",
        scope=["openid", "email", "profile"],
    )
    return redirect(request_uri)




@app.route("/log-in/callback")
def callback():
    # Get authorization code Google sent back to you
    code = request.args.get("code")

    # Find out what URL to hit to get tokens that allow you to ask for
    # things on behalf of a user
    google_provider_cfg = get_google_provider_cfg()
    token_endpoint = google_provider_cfg["token_endpoint"]

    # Prepare and send request to get tokens! Yay tokens!
    token_url, headers, body = client.prepare_token_request(
        token_endpoint,
        authorization_response=request.url,
        redirect_url=request.base_url,
        code=code,
    )
    token_response = requests.post(
        token_url,
        headers=headers,
        data=body,
        auth=(GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET),
    )

    # Parse the tokens!
    client.parse_request_body_response(json.dumps(token_response.json()))

    # Now that we have tokens (yay) let's find and hit URL
    # from Google that gives you user's profile information,
    # including their Google Profile Image and Email
    userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
    uri, headers, body = client.add_token(userinfo_endpoint)
    userinfo_response = requests.get(uri, headers=headers, data=body)

    # We want to make sure their email is verified.
    # The user authenticated with Google, authorized our
    # app, and now we've verified their email through Google!
    if userinfo_response.json().get("email_verified"):
        unique_id = userinfo_response.json()["sub"]
        users_email = userinfo_response.json()["email"]
        picture = userinfo_response.json()["picture"]
        users_name = userinfo_response.json()["given_name"]
        if users_email == "test@constructeducation.com":
           role ="FIN"
        else:
            role = "BASE"
    else:
        return "User email not available or not verified by Google.", 400



    # Create a user in our db with the information provided
    # by Google
    user = User(
        id_=unique_id, name=users_name, email=users_email, profile_pic=picture, role=role
    )

    # Doesn't exist? Add to database
    if not User.get(unique_id):
        User.create(unique_id, users_name, users_email, picture, role)

    # Begin user session by logging the user in
    login_user(user)

    # Send user back to homepage
    return redirect(url_for("index"))


# # the route "/logout" being used already, by Cubes

@app.route("/log-out")
@login_required(role="ANY")
def logout():
    logout_user()
    return redirect(url_for("index"))


def get_google_provider_cfg():
    return requests.get(GOOGLE_DISCOVERY_URL).json()


if __name__ == "__main__":
    app.run(ssl_context="adhoc")


