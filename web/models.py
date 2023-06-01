from web import db,bcrypt,login_manager
from datetime import datetime
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)
    
class User(db.Model,UserMixin):
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(50),nullable=False,unique=True)
    password_hash = db.Column(db.String(60))
    pastes = db.relationship("Paste")
    
    @property
    def password(self):
        return self.password
    
    @password.setter
    def password(self,plain_text):
        self.password_hash = bcrypt.generate_password_hash(plain_text).decode('utf-8')

    def check_password(self,plain_text):
        return bcrypt.check_password_hash(self.password_hash,plain_text)
    
#===========================================

class Paste(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    pid = db.Column(db.String(24),nullable=False,unique=True)
    title = db.Column(db.String(256),nullable=False)
    text = db.Column(db.Text)
    date = db.Column(db.Date,nullable=False,default=datetime.now().date())
    user = db.Column(db.Integer,db.ForeignKey('user.id'),default=0)

    def __repr__(self):
        return f'Paste({self.id},{self.pid})'