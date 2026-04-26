"""
This module contains all routes that handle creation, modification and removal of shelves in the database.
"""

import math
from flask import Blueprint, session, url_for, redirect, request
from src.services import shelf
from src.services.user import login_required, csrf_required

shelf_bp = Blueprint('shelf', __name__)

@shelf_bp.post("/create_shelf")
@login_required
@csrf_required
def create_shelf():
    """Route for creating a new bookshelf"""
    username = session["username"]
    user_id = session["user_id"]

    name = request.form["name"]
    description = request.form["description"]
    public = 1 if request.form.get("public-choice") else 0

    page_size = 10
    shelf_count = shelf.get_number_of_all_shelves(user_id)
    page_count = math.ceil(shelf_count / page_size)
    page_count = max(page_count, 1)

    try:
        shelf.create_shelf(user_id, name, description, public)
    except Exception:
        return redirect(url_for("view.index"))

    return redirect(url_for("view.shelves",
                            username=username,
                            page_count=page_count,
                            page=1))

@shelf_bp.get("/remove_shelf/<username>/<shelf_id>")
@login_required
def remove_shelf(username, shelf_id):
    """
    Route for removing a bookshelf

    Args:
        username (str): username of the current user
        shelf_id (int): Id of the shelf
    """
    try:
        shelf.delete_shelf(shelf_id)
    except Exception:
        return redirect(url_for("view.index"))

    return redirect(url_for("view.shelves", username=username))
