from flask import Flask, request, render_template, make_response
import requests
import os
import sqlite3

app = Flask(__name__)

conn = sqlite3.connect('twitter.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS tweets (id INTEGER PRIMARY KEY AUTOINCREMENT, tweet text, user INTEGER, FOREIGN KEY(user) REFERENCES user(id))''');
c.execute('''CREATE TABLE IF NOT EXISTS user (id INTEGER PRIMARY KEY AUTOINCREMENT, full_name text, username text NOT NULL UNIQUE, password text)''')
conn.commit()
conn.close()

@app.route("/")
def home():
	return render_template('base.html')

@app.route('/twitter_clone', methods=["POST", "GET"])
def twitter_clone():
	if request.method == 'POST':
		conn = sqlite3.connect('twitter.db')
		c = conn.cursor()
		my_text = request.form['text']
		username = request.cookies.get('username')
		userr = c.execute("select id from user where username = '{}'".format(username)).fetchone()[0]
		c.execute("INSERT INTO tweets (tweet, user) values (?, ?)", (my_text, userr))
		conn.commit()
		all_tweets = c.execute('SELECT * FROM tweets where user = {}'.format(userr)).fetchall()
		conn.close()
		return render_template('view_tweets.html', tweets=all_tweets)
	else:
		return render_template('analyzer.html')

@app.route('/register', methods=["POST", "GET"])
def register():
	conn = sqlite3.connect('twitter.db')
	c = conn.cursor()
	if request.method == 'POST':
		full_name = request.form['full_name']
		username = request.form['username']
		password = request.form['password']
		c.execute("INSERT INTO user (full_name, username, password) values (?, ?, ?)", (full_name, username, password))
		conn.commit()
		conn.close()
		resp = make_response(render_template('loggedin.html'))
		resp.set_cookie('username', username)
		return resp
	return render_template('register.html')

@app.route('/login', methods=['POST', 'GET'])
def login():
	if request.method == 'POST':
		username = request.form['full_name']
		password = request.form['password']
		if c.execute("select username from user where '{}' in (select password from user where username = '{}')".format(password, username)).fetchall() != null:
			return render_template('loggedin.html')
		else:
			return render_template('re-loggin.html')
	else:
		return render_template('login.html')

@app.route('/loggedin')
def get_tweets():
	return render_template('/loggedin.html')

@app.route('/view_tweets')
def view_tweets():
	username = request.cookies.get('username')
	conn = sqlite3.connect('twitter.db')
	c = conn.cursor()
	tweets = c.execute("select tweet from tweets where user in (select id from user where username = '{}')".format(username)).fetchall()
	conn.close()
	return render_template('/view_tweets.html', username=username, tweets=tweets)

if __name__ == '__main__':
	app.run()

