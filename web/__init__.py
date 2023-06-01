import os
from flask import Flask,render_template
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']=f'sqlite:///{os.path.join(os.getcwd(),"database.db")}'
app.config['SECRET_KEY']='SECRET_KEY_HERE'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
#====== Blueprint
from web.routes.views import views
from web.routes.auth import auth
app.register_blueprint(views,url_prefix='/')
app.register_blueprint(auth,url_prefix='/')

#====== Database
from web.models import Paste,User
with app.app_context():
    #db.drop_all()
    db.create_all()

#========
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.jinja'),404