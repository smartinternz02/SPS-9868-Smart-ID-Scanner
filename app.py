# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
from views import get_attendence
import mysql.connector
import io


app = Flask(__name__)
app.config['MYSQL_HOST'] = 'remotemysql.com'
app.config['MYSQL_USER'] = 'Zic0pVSRrN'
app.config['MYSQL_PASSWORD'] = '3wAB5s7wYS'
app.config['MYSQL_DB'] = 'Zic0pVSRrN'
mysql = MySQL(app)
app.secret_key = 'a'

@app.route('/')

def homer():
    return render_template('home.html')

@app.route('/signup',methods =['GET', 'POST'])
def signup():
    msg = ''
    if request.method == 'POST' :
        name = request.form['name']
        email = request.form['email']
        mobile = request.form['mobile']
        password = request.form['password']
       
        session["name"] = name
        cursor = mysql.connection.cursor()
        cursor.execute('INSERT INTO user VALUES ( NULL, % s, % s, % s, % s)', (name, email,mobile,password))
        mysql.connection.commit()
        msg = 'You have successfully registered ! Sign in Now'
    return render_template('sign.html', msg = msg)




@app.route('/login', methods =['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'name' in request.form and 'password' in request.form:
        name = request.form['name']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM user WHERE name = % s AND password = % s', (name, password ))
        account = cursor.fetchone()
        if account:
            session['loggedin'] = True
            session['id'] = account['id']
            userid=  account['id']
            session['username'] = account['name']
            msg = 'Logged in successfully !'
            return render_template('upload.html', msg = msg)
        else:
            msg = 'Incorrect username / password !'
    return render_template('sign.html', msg = msg)
  

@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('name', None)
    return render_template('home.html')



@app.route('/filehtml')
def filehtml():
    return render_template('file.html')

@app.route('/home')
def home():
    return render_template('upload.html')




ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])





def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# route and function to handle the upload page
@app.route('/fileupload', methods=['GET', 'POST'])
def upload_page():
    if request.method == 'POST':
        # check if there is a file in the request
        if 'file' not in request.files:
            return render_template('upload.html', msg='No file selected')
        file1 = request.files['file']
       
        # if no file is selected
        if file1.filename == '':
            return render_template('upload.html', msg='No file selected')

        if file1 and allowed_file(file1.filename):
            

            # call the OCR function on it
            extracted_text = get_attendence(file1)
           
            #extracted_text = get_text_from_api(file)
            
            data=extracted_text
            
            cursor = mysql.connection.cursor()
            
            SQLInsertCmd = """INSERT INTO
                 exdata VALUES (%s,%s)"""
            cursor.execute(SQLInsertCmd,(session['id'],data,))
            mysql.connection.commit()
  
# Execute the query and commit the database.
           
           
            
            # extract the text and display it
            return render_template('file1.html',
                                   msg='Successfully processed',
                                   extracted_text=extracted_text,
                                   )
    elif request.method == 'GET':
        return render_template('upload.html')


@app.route('/viewhistory')
def viewhistory():
    print(session["username"],session['id'])
    
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT data FROM exdata WHERE userid = % s', (session['id'],))
    account = cursor.fetchall()
    
    

    
    return render_template('viewhistory.html',account = account)














if __name__ == '__main__':
   app.run(debug = True)
