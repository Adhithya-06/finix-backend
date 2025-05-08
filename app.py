from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import db
from routes import transaction_routes
from ai_routes import ai_routes 
from flask_migrate import Migrate


app = Flask(__name__)
CORS(app)

# Database Configuration (using SQLite)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db' 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database
db.init_app(app)

# ✅ Initialize Flask-Migrate
migrate = Migrate(app, db)

# Register routes
app.register_blueprint(transaction_routes)
app.register_blueprint(ai_routes, url_prefix='/ai')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)