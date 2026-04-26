"""
This module contains all routes that handle creation of, and logging in/out users.
"""

from flask import Blueprint, session, url_for, redirect, request
import secrets
from src.services import user
from src.services.user import login_required

user_bp = Blueprint('user', __name__)

@user_bp.post("/create")
def create():
    """Route for creating a new user"""

    username = request.form["username"]
    password1 = request.form["password1"]
    password2 = request.form["password2"]

    if password1 != password2:
        session["register_message"] = "VIRHE! salasanat eivät ole samat"
        return redirect(url_for("view.register"))

    try:
        user.create_user(username, password1)
    except Exception:
        return redirect(url_for("view.register"))

    session["login_message"] = "Käyttäjä luotu!"
    return redirect(url_for("view.index"))

@user_bp.post("/login")
def login():
    """Route for logging in user"""

    username = request.form["username"]
    password = request.form["password"]

    session["csrf_token"] = secrets.token_hex(16)

    if user.login(username, password):
        return redirect(url_for("view.profile", username=username))
    else:
        return redirect(url_for("view.index"))

@user_bp.get("/logout")
@login_required
def logout():
    """Route for logging out user"""

    del session["username"]
    return redirect(url_for("view.index"))
