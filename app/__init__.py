from flask import Flask
from flask_cors import CORS
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

def create_app():
    root_dir = Path(__file__).parent.parent
    
    app = Flask(__name__,
                template_folder=str(root_dir / 'templates'),
                static_folder=str(root_dir / 'static'))
    
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')
    app.config['JSON_SORT_KEYS'] = False
    
    CORS(app)
    
    from app.routes import api_bp
    app.register_blueprint(api_bp, url_prefix='/api')
    
    return app
