from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_login import LoginManager
from web.config import Config
app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
mail = Mail(app)
login_manager = LoginManager(app)
login_manager.login_view = 'adminLog.index_admin'


import web.views
import web.routes
from web.admin.routes import adminLog

app.register_blueprint(adminLog, url_prefix="/admin")
