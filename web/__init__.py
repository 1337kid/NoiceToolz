import os
from dotenv import dotenv_values
from flask import Flask,render_template
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_minify import Minify

config = dotenv_values(".env")
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']=config['SQLALCHEMY_DATABASE_URI']
app.config['SECRET_KEY']=config['SECRET_KEY']
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
Minify(app=app, html=True, cssless=True)
#====== Blueprint
from web.routes.views import views
from web.routes.auth import auth
app.register_blueprint(views,url_prefix='/')
app.register_blueprint(auth,url_prefix='/')

#====== Database
from web.models import Paste,User
with app.app_context():
    db.drop_all()
    db.create_all()
    guest = User(id=0,username='guest',password_hash=None)
    db.session.add(guest)
    db.session.commit()

#====== Error pages
@app.errorhandler(404)
def page_not_found(e):
    return render_template('errorpages/404.jinja'),404

@app.errorhandler(401)
def page_not_found(e):
    return render_template('errorpages/401.jinja'),401