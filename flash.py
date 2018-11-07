from flask import Flask, flash,make_response, redirect, render_template,render_template_string, request, url_for,g
from flask_socketio import SocketIO
import sqlite3,json,os,random, sys 
from lib import transposition


DATABASE = 'data/database.db'
transpositioncipher=transposition
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def query_db(query, args=(), one=False):
    db = get_db()
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    #print(rv)
    db.commit()
    cur.close()
    return (rv[0] if rv else None) if one else rv
def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('data/schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()
def save_theme(request,theme_id):
    db = get_db()
    

    query="UPDATE themes SET `gjs-assets` = '"+request['gjs-assets']+"', `gjs-css` = '"+request['gjs-css']+"',`gjs-styles`='"+request['gjs-styles']+"',`gjs-html`='"+request['gjs-html']+"',`gjs-components`='"+request['gjs-components']+"' WHERE id="+str(theme_id)
    #query="alter table themes add column `gjs-components` TEXT"
    print(query);
    cur = get_db().execute(query)
    #rv = cur.fetchall()
    #print(rv)
    db.commit()
    cur.close()
def create_template(template,wp_template,args):
    path=wp_template[:wp_template.rfind('/')]
    print(path)
    if not os.path.exists(path):
        os.makedirs(path)
        #print("File exist")
    rendered=render_template(template,themevalue=args)
    file = open(wp_template,'w+') 
    file.write(rendered)
    file.close() 
@app.route('/')
def index():
   return render_template('index.html')
@app.route('/caesar-cipher',methods = ['GET', 'POST'])
def caesar():
    return render_template('caesar.html')
@app.route('/theme',methods = ['GET', 'POST'])
def theme():
    if request.method == 'POST':
        sql="INSERT INTO themes (value) VALUES ('"+json.dumps(request.form)+"')"
        theme = query_db(sql)
        return render_template('theme.html')
    else:
        sql="select * from themes where ID=?"
        theme = query_db(sql,[9], one=True)
        allthemes=[]
        for row in query_db('select * from themes'):
            print(row)
            try:
                if json.loads(row[1]):
                    allthemes.append({'id':row[0],'name':json.loads(row[1])['theme_name']})
            except ValueError:
                print("Error")
        themevalue=json.loads(theme[1])
        #print(themevalue['theme_name'])
        return render_template('theme.html',themevalue=themevalue,allthemes=allthemes)
@app.route('/wordpress/generate',methods = ['GET'])
def wordpressGenerate():
    if request.method == 'POST':
        if request.form['theme']:
            sql="select * from themes where ID=?"
            theme = query_db(sql,[request.form['theme']], one=True)
            themevalue=json.loads(theme[1])
            for path, subdirs, files in os.walk('templates/wordpress/Foundation'):
                for name in files:
                    #print (os.path.join(path, name))
                    template_path=os.path.join(path, name)
                    create_template(template_path[10:],'themes/wordpress/'+themevalue['theme_name']+template_path[30:],themevalue)
            return render_template('grapeedit.html',themevalue=themevalue)
    return render_template('grapeedit.html')

@app.route('/magento/generate',methods = ['GET'])
def magentoGenerate():
    if request.method == 'POST':
        if request.form['theme']:
            sql="select * from themes where ID=?"
            theme = query_db(sql,[request.form['theme']], one=True)
            themevalue=json.loads(theme[1])
            for path, subdirs, files in os.walk('templates/wordpress/Foundation'):
                for name in files:
                    #print (os.path.join(path, name))
                    template_path=os.path.join(path, name)
                    create_template(template_path[10:],'themes/wordpress/'+themevalue['theme_name']+template_path[30:],themevalue)
            return render_template('grapeedit.html',themevalue=themevalue)
    return render_template('grapeedit.html')
@app.route('/theme/edit',methods = ['POST','GET'])
def grapeedit():
    if request.method == 'POST':
        if request.form['theme']:
            sql="select * from themes where ID=?"
            theme = query_db(sql,[request.form['theme']], one=True)
            themevalue=json.loads(theme[1])
            for path, subdirs, files in os.walk('templates/wordpress/Foundation'):
                for name in files:
                    #print (os.path.join(path, name))
                    template_path=os.path.join(path, name)
                    create_template(template_path[10:],'themes/wordpress/'+themevalue['theme_name']+template_path[30:],themevalue)


            
            #create_template('header.php',themevalue['theme_name']+'/header.php',themevalue)
            #create_template('template-full-width.html',themevalue['theme_name']+'/template-full-width.php',themevalue)
            #create_template('style.css',themevalue['theme_name']+'/style.css',themevalue)

            #print(rendered);
            return render_template('grapeedit.html',themevalue=themevalue)
    return render_template('grapeedit.html')

@app.route('/theme/store',methods = ['POST'])
def store():
    save_theme(request.form,request.args.get('id'))
    #return render_template('wordpress-generate.html')

    error = None
    return render_template('login.html', error = error)
@app.route('/theme/load',methods = ['GET'])
def load():
    theme_id=request.args.get('id')

    sql="select `gjs-assets`,`gjs-css`,`gjs-styles`,`gjs-components`,`gjs-html` from themes where ID=?"

    
    theme = query_db(sql,[theme_id], one=True)
    resp = make_response(json.dumps({'gjs-assets':theme[0],'gjs-css':theme[1],'gjs-styles':theme[2],'gjs-components':theme[3],'gjs-html':theme[4]}), 200)
    resp.headers['Content-Type'] = 'application/json'
    return resp
    return json.dumps({'gjs-assets':theme[0],'gjs-css':theme[1],'gjs-styles':theme[2],'gjs-components':theme[3]})

@app.route('/transposition-cipher',methods = ['GET', 'POST'])
def transposition():
    if request.method == 'POST':
        if request.form['message']:
            translated=transpositioncipher.encryptMessage(4,request.form['message'])
            return render_template('transposition.html',translated = translated)
    return render_template('transposition.html')
@socketio.on('message')
def handle_message(message):
    print('received message: ' + message)
@app.route('/login', methods = ['GET', 'POST'])
def login():
   error = None
   
   if request.method == 'POST':
      if request.form['username'] != 'admin' or \
         request.form['password'] != 'admin':
         error = 'Invalid username or password. Please try again!'
      else:
         flash('You were successfully logged in')
         return redirect(url_for('index'))
   return render_template('login.html', error = error)
if __name__ == "__main__":
  app.run(debug = True)