from flask import Blueprint,render_template,request,redirect,url_for,make_response,flash
from web.forms import CreatePasteForm
from web.models import Paste,User
from web import db
from flask_login import current_user,login_required
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
    if username=='guest': user=User(id=0,username='guest')
    else: user = User.query.filter_by(username=username).first_or_404()
    pastes = Paste.query.filter_by(user=user.id).all()
    return render_template('user.jinja',pastes=pastes[::-1],user=user)

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
        else: return render_template('paste.jinja',paste=paste,size=len(paste.text),user=user)

@views.route('/editpaste/<pid>',methods=['POST','GET'])
@login_required
def edit_paste(pid):
    form = CreatePasteForm()
    paste = Paste.query.filter_by(pid=pid).first()
    if current_user.id == paste.user:
        if form.validate_on_submit():
            paste.title = form.title.data
            print(form.title.data)
            paste.text = form.text.data
            db.session.commit()
            return redirect(url_for('views.view_paste',pid=pid))
    else:
        flash('You dont have permission to edit this paste',category='danger')
        return redirect(url_for('views.view_paste',pid=pid))
    return render_template('edit_paste.jinja',form=form,paste=paste)

@views.route('/deletepaste/<pid>')
@login_required
def delete_paste(pid):
    paste = Paste.query.filter_by(pid=pid).first()
    if current_user.id==paste.user:
        db.session.delete(paste)
        db.session.commit()
        flash(f'Paste with ID "{pid}" was deleted',category='success')
        return redirect(url_for('views.view_user',username=current_user.username))
    else:
        flash(f"You don't have permission to delete the paste with id \"{pid}\"",category='danger')
        return redirect(url_for('views.view_paste',pid=pid))