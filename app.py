from flask import Flask,request,render_template,redirect,url_for,make_response,session
from flask_minify import minify
from werkzeug.security import generate_password_hash,check_password_hash
from core.main import *
from core.dbcon import *
from core.config import SECRET_KEY
import validators

setup_db()
app=Flask(__name__)
minify(app=app, html=True, cssless=True)
home_page_texts=read_yml('data/home_page.yml')
app.secret_key=SECRET_KEY
#=========
@app.route('/')
def action():
    reqargs=request.args.to_dict()
    if reqargs:
        if 'action' in reqargs:
            if reqargs['action']=='paste':return render_template('notebin/createpaste.html')
            elif reqargs['action']=='shrink':return render_template('urlshrink/createlink.html')
        return redirect('/',code=302)
    return render_template('home.html',texts=home_page_texts)

@app.route('/createpost',methods=['POST'])
def create():
    title=request.form['title']
    record = request.form['content']
    record=base64_dec_enc(record,True)
    title=base64_dec_enc(title,True)
    postid=generate_rand_id(16)
    conn,cur=get_db_connection()
    cur.execute("INSERT INTO notes VALUES (%s,%s,%s)",(postid,title,record))
    conn.commit()
    conn.close()
    return redirect(f"/p/{postid}", code=302)

@app.route('/p/<pid>',methods=['GET'])
def get_data(pid):
    conn,cur=get_db_connection()
    reqargs=request.args.to_dict()
    cur.execute('select title,content from notes where id = %s',(pid,))
    paste=cur.fetchone()
    conn.close()
    if paste==None:return render_template('notebin/createpaste.html',paste=True,title="Paste Not Found",content="The requested paste was not found on this server",paste_size=0)
    title=base64_dec_enc(paste[0],False)
    post=base64_dec_enc(paste[1],False)
    if 'raw' in reqargs and reqargs['raw']=='true':
        response = make_response(post, 200)
        response.mimetype = "text/plain"
        return response
    raw_url=url_for('get_data',pid=pid)+'?raw=true'
    return render_template('notebin/createpaste.html',paste=True,title=title,content=post,raw_url=raw_url,paste_size=len(post.encode('utf-8')))

@app.route('/r/<rid>')
def get_link(rid):
    conn,cur=get_db_connection()
    reqargs=request.args.to_dict()
    cur.execute('select link from links where id = %s',(rid,))
    url=cur.fetchone()
    conn.close()
    if url is None:return redirect('/',code=302)
    url=base64_dec_enc(url[0],False)
    return redirect(url, code=302)

@app.route('/createlink',methods=['POST','GET'])
def create_link():
    url=request.form['url']
    print(validators.url(url))
    if validators.url(url)!=True:
        return render_template('urlshrink/createlink.html',error=True)
    url=base64_dec_enc(url,True)
    linkid=generate_rand_id(6)
    conn,cur=get_db_connection()
    cur.execute("INSERT INTO links VALUES (%s,%s)",(linkid,url))
    conn.commit()
    conn.close()
    return render_template('urlshrink/createlink.html', link=url_for('get_link',rid=linkid,_external=True))

@app.route('/admin/',methods=['POST','GET'])
def admin():
    if request.method=='GET' and 'username' in session:
        reqargs=request.args.to_dict()
        if 'delete' in reqargs:
            if reqargs['delete']=='paste':
                paste_ids=admin_db_select('notes')
                return render_template('admin/delrec.html',delete='paste',data=paste_ids,admin_login=1,lolvar="Note Bin")
            elif reqargs['delete']=='url':
                url_ids=admin_db_select('links')
                return render_template('admin/delrec.html',delete='url',data=url_ids,admin_login=1,lolvar="URL Shrink")
        return render_template('admin/admin.html',admin_login=1)
    if request.method=='POST':
        if not 'username' in session:
            passwd=request.form['password']
            username=request.form['username']
            conn,cur=get_db_connection()
            cur.execute('select password from admin where username = %s',(username,))
            adm_passwd=cur.fetchone()
            conn.close()
            if adm_passwd==None:return render_template('admin/login.html',error='Username not found')
            elif check_password_hash(adm_passwd[0],passwd):
                session['username']=username
                return render_template('admin/admin.html',admin_login=1)
            else:return render_template('admin/login.html',error='Incorrect password')
    return render_template('admin/login.html')

@app.route('/admin/delete')
def admin_delete():
    if 'username' in session:
        reqargs=request.args.to_dict()
        if reqargs['service']=='paste':
            admin_db_remove('notes',reqargs['id'])
            return redirect('/admin?delete=paste',302)
        elif reqargs['service']=='url':
            admin_db_remove('links',reqargs['id'])
            return redirect('/admin/?delete=url',302)
    return redirect('/admin',302)

@app.route('/admin/newcreds',methods=['POST'])
def newcreds():
    passwd=request.form['password']
    username=request.form['username']
    conn,cur=get_db_connection()
    passwd=generate_password_hash(passwd,"sha256")
    cur.execute('update admin set username=%s,password=%s where id=1',(username,passwd))
    conn.commit()
    conn.close()
    return redirect('/admin')

@app.route('/admin/logout')
def logout():
    session.pop('username',None)
    return redirect('/admin')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'),404

if __name__=='__main__':
    app.run(threaded=True)