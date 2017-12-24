from flask import Flask,render_template , redirect, url_for,request , g ,session,request
import sqlite3
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

def validate(username,password):
	con = sqlite3.connect('static/User.db')
	completion = False
	with con:
		cur = con.cursor()
		cur.execute("SELECT * FROM USERS");
		rows = cur.fetchall()
		for row in rows:
			dbUser = row[0]
			dbPass = row[1]

			if dbUser == username and dbPass == password:
				session['user'] = request.form['username']
				completion = True

	return completion


@app.route('/',methods=['GET','POST'])
def index():
	error = None
	if request.method == 'POST':
		session.pop('user',None)
		username = request.form['username']
		password = request.form['password']

		completion = validate(username,password)

		if completion == False:
			error = 'Invalid Credentials , Please try again'
		else:
			return redirect(url_for('secret'))

	return render_template('index.html',error=error)



@app.route('/secret')
def secret():
	if g.user:
		return render_template('protected.html')

	return redirect(url_for('index'))


@app.before_request
def before_request():
	g.user = None
	if 'user' in session:
		g.user = session['user']


@app.route('/getsession')
def getsession():
	if 'user' in session:
		return session['user']

	return 'Not logged in !'

@app.route('/dropsession')
def dropsession():
	session.pop('user',None)
	return 'Dropped!'


if __name__ == '__main__':
	app.run(debug=True)