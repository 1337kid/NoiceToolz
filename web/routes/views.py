from flask import Blueprint,render_template,request,redirect,url_for,make_response
from web.forms import CreatePasteForm
from web.models import Paste,User
from web import db
from flask_login import current_user
import string,random

views = Blueprint('views',__name__)

def gen_pid():
    chars=string.ascii_letters+'1234567890'
    id = ''
    for _ in range(24):
        id+=random.choice(chars)
    return id

@views.route('/',methods=['GET','POST'])
def home_page():
    form = CreatePasteForm()
    if request.method=='POST':
        if form.validate_on_submit():
            title = form.title.data
            text = form.text.data
            #===
            if not current_user.is_active: user_id=0
            else: user_id=current_user.id 
            #===
            new_paste = Paste(title=title,text=text,user=user_id,pid=gen_pid())
            db.session.add(new_paste)
            db.session.commit()
            return redirect(url_for('views.view_paste',pid=new_paste.pid))

    elif request.method=='GET':
        return render_template('home.jinja',form=form)

@views.route('/user/<string:username>/')
def view_user(username):
    if username=='guest': user=0
    else: user = User.query.filter_by(username=username).first_or_404().id
    pastes = Paste.query.filter_by(user=user).all()
    return render_template('user.jinja',pastes=pastes[::-1],user=username)

@views.route('/paste/<string:pid>')
def view_paste(pid):
    reqargs=request.args.to_dict()
    paste = Paste.query.filter_by(pid=pid).first_or_404()
    if paste:
        user = User.query.filter_by(id=paste.user).first()
        if not user: user='guest'
        else: user=user.username
        if 'raw' in reqargs and reqargs['raw']=='true':
            response = make_response(paste.text, 200)
            response.mimetype = "text/plain"
            return response
        else: return render_template('post.jinja',paste=paste,size=len(paste.text),user=user)