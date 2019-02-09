from flask import Flask, request, render_template
import requests
import os
import sqlite3

app = Flask(__name__)

conn = sqlite3.connect('twitter.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS tweets (id INTEGER PRIMARY KEY AUTOINCREMENT, tweet text)''');
conn.commit()
conn.close()

@app.route("/")
def home():
	return render_template('base.html')

@app.route('/twitter_clone', methods=["POST", "GET"])
def twitter_clone():
	conn = sqlite3.connect('twitter.db')
	c = conn.cursor()
	if request.method == 'POST':
		my_text = request.form['text']
		c.execute("INSERT INTO tweets (tweet) values (?)", (my_text,))
		conn.commit()
	all_tweets = c.execute('SELECT * FROM tweets').fetchall()
	conn.close()
	return render_template('analyzer.html', all_tweets=all_tweets)

if __name__ == '__main__':
	app.run()

