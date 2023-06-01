from flask import Blueprint,request,redirect,render_template,flash,url_for
from web.forms import LoginForm,SignUpForm
from web.models import User
from web import db
from flask_login import login_user, logout_user

auth = Blueprint('auth',__name__)

@auth.route('/login/',methods=['POST','GET'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user.check_password(form.password.data):
            login_user(user)
            return redirect(url_for('views.home_page')),302
        else:  flash('Incorrect password',category='danger')

    if form.errors!={}:
        for error in form.errors.values():
            flash(error[0],category='danger')

    return render_template('auth/login.jinja',form=form)

@auth.route('/signup/',methods=['POST','GET'])
def signup_page():
    form = SignUpForm()
    if form.validate_on_submit():
        new_user = User(username=form.username.data,
                        password=form.password1.data
                        )
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        return redirect(url_for('views.home_page')),302
    
    if form.errors!={}:
        for error in form.errors.values():
            flash(error[0],category='danger')

    return render_template('auth/signup.jinja',form=form)

@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('views.home_page')),302