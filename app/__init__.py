from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

login = LoginManager(app)
login.login_view = 'auth.login'
login.login_message_category = 'is-danger'

from app.blueprints.auth import auth
app.register_blueprint(auth)

from app.blueprints.inventory import inventory
app.register_blueprint(inventory)

from app import routes
