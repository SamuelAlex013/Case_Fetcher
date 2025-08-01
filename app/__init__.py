import os
from flask import Flask

def create_app():
    # Explicitly set the template folder to be relative to the project root
    template_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'templates'))
    app = Flask(__name__, template_folder=template_folder)
    
    from app.routes import main
    app.register_blueprint(main)

    return app