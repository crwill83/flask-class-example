from flask import Flask
from config import Config

# import our blueprints
from .auth.routes import auth
from .ig.routes import ig
from .shop.routes import shop
from .pokemon.routes import pokemon

# import our db related
from .models import db, User
from .auth.routes import mail
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail

app  = Flask(__name__)
login = LoginManager()

@login.user_loader
def load_user(user_id):
    return User.query.get(user_id)

app.register_blueprint(auth)
app.register_blueprint(ig)
app.register_blueprint(shop)
app.register_blueprint(pokemon)

app.config.from_object(Config)

# initialize our database to work with our app
db.init_app(app)
login.init_app(app)
mail.init_app(app)

login.login_view = "auth.logMeIn"

migrate = Migrate(app, db)

from . import routes
from . import models