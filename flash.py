from flask import Flask, flash, redirect, render_template,render_template_string, request, url_for,g
from flask_socketio import SocketIO
import sqlite3,json
from lib import transposition


import random, sys 
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
@app.route('/')
def index():
   return render_template('index.html')
@app.route('/caesar-cipher',methods = ['GET', 'POST'])
def caesar():
    return render_template('caesar.html')
@app.route('/wordpress',methods = ['GET', 'POST'])
def wordpress():
    if request.method == 'POST':
        sql="INSERT INTO themes (value) VALUES ('"+json.dumps(request.form)+"')"
        theme = query_db(sql)
        return render_template('wordpress.html')
    else:
        sql="select * from themes where ID=?"
        theme = query_db(sql,[9], one=True)
        allthemes=[]
        for row in query_db('select * from themes'):
            try:
                if json.loads(row[1]):
                    allthemes.append({'id':row[0],'name':json.loads(row[1])['theme_name']})
            except ValueError:
                print("Error")
        themevalue=json.loads(theme[1])
        #print(themevalue['theme_name'])
        return render_template('wordpress.html',themevalue=themevalue,allthemes=allthemes)
@app.route('/wordpress/generate',methods = ['POST'])
def generate():
    if request.method == 'POST':
        if request.form['theme']:
            sql="select * from themes where ID=?"
            theme = query_db(sql,[request.form['theme']], one=True)
            themevalue=json.loads(theme[1])
            rendered=render_template('wordpress/theme.html',themevalue=themevalue)
            file = open("themes/wordpress/index.php",'w+') 
            file.write(rendered)
            file.close() 

            #print(rendered);
            return render_template('wordpress-generate.html',themevalue=themevalue)
    return render_template('wordpress-generate.html')
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