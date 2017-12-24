from flask import Flask, render_template, redirect, url_for, request, g
import sqlite3
import hashlib
import subprocess

app = Flask(__name__)


def validate(username, password):
    con = sqlite3.connect('static/User.db')
    completion = False
    with con:
                cur = con.cursor()
                cur.execute("SELECT * FROM USERS")
                rows = cur.fetchall()
                for row in rows:
                    dbUser = row[0]
                    dbPass = row[1]
                    if dbUser==username and dbPass==password:
                        completion = True

                #print "Database password "+str(dbPass)
                #print dbUser
    return completion


@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        #print username
        #print password
        completion = validate(username, password)
        #print completion
        if completion ==False:
            error = 'Invalid Credentials. Please try again.'
        else:
            return redirect(url_for('secret'))
    return render_template('newlogin.html', error=error)


@app.route('/secret')
def secret():
    return render_template('secret.html')


@app.route("/echo", methods=['POST'])
def echo(): 
    ipaddress = request.form['text']
    cmd = ["python","/home/cnadmin/work/snmp/test.py",ipaddress]
    p = subprocess.Popen(cmd,stdout=subprocess.PIPE,
    					stderr=subprocess.PIPE,
    					stdin=subprocess.PIPE)
    out,err = p.communicate()
    display = '<h2>'+"Installed Software list"+'</h2>'
    lines   = "=================================================================================================================================="+'<br/>'
    msg = display +lines+ out
    return '<pre>'+msg+'</pre>'


if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port=80)
