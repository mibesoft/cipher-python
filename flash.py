from flask import Flask, flash, redirect, render_template, request, url_for

import random, sys, transposition
transpositioncipher=transposition
app = Flask(__name__)
app.secret_key = 'random string'

@app.route('/')
def index():
   return render_template('index.html')
@app.route('/caesar-cipher',methods = ['GET', 'POST'])
def caesar():
    return render_template('caesar.html')
@app.route('/transposition-cipher',methods = ['GET', 'POST'])
def transposition():
    if request.method == 'POST':
        if request.form['message']:
            translated=transpositioncipher.encryptMessage(4,request.form['message'])


            return render_template('transposition.html',translated = translated)
        
    return render_template('transposition.html')

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
