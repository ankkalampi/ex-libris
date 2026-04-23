import sys
from pathlib import Path
from flask import Flask
from flask import session, g
import config

sys.path.append(str(Path(__file__).parent / "src"))

from src.routes.view_routes import view_bp
from src.routes.user_routes import user_bp
from src.routes.book_routes import book_bp
from src.routes.shelf_routes import shelf_bp

app = Flask(__name__)
app.secret_key = config.secret_key
app.register_blueprint(view_bp)
app.register_blueprint(user_bp)
app.register_blueprint(book_bp)
app.register_blueprint(shelf_bp)

@app.before_request
def load_logged_in_user():
    """
    Sets the user variable for g object before a request is made
    """
    username = session.get("username")
    if username is None:
        g.user = None
    else:
        g.user = username
