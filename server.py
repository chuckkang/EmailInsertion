from flask import Flask, render_template, request, redirect, session, flash
from mysqlconnection import MySQLConnector
import random
from datetime import datetime
import re
import md5 # imports the md5 module to generate a hash
import os, binascii # salt, salt = binascii.b2a_hex(os.urandom(15)), then password = md5.new(password+salt).hexdigest()

app = Flask(__name__)
app.secret_key = " this is the secret key"
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
mysql = MySQLConnector(app,'friendsdb') #set up the sql connection.  it will return a sql connection

@app.route('/', methods=['POST', 'GET'])
def index():
	
	sql = "SELECT friends.first_name, friends.last_name, friends.email from friends"
	db = mysql.query_db(sql)
	email = ''
	if request.method=="POST":
		email = request.form['email'].strip()
		if EMAIL_REGEX.match(email) :
			session['email'] = email
			return redirect ('/insert')
		else:
			
			flash("Please enter a valid email")

	return render_template("index.html", data=db, email=email)

@app.route('/insert')
def update_email():
	
	email = session['email']
	sql = "INSERT into friends(email) values(:email)"
	data = {'email': email}
	db = mysql.query_db(sql, data)
	flash("YES YOU INSERTED THE EMAIL ADDRESS!")
	return redirect ("/")

app.run(debug=True) # run our server