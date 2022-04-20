from flask import Flask, render_template, request, redirect, session, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)
app.secret_key = "Secret One"
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/authentication_api'
db = SQLAlchemy(app)


class Userdetails(db.Model):
    SNo = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(40), unique=False, nullable=False)
    DOB = db.Column(db.String(12), unique=False, nullable=False)
    Email = db.Column(db.String(20), unique=True, nullable=False)
    Username = db.Column(db.String(20), unique=True, nullable=False)
    Password = db.Column(db.String(25), unique=False, nullable=False)
    Date = db.Column(db.String(12), unique=False, nullable=True)


@app.route('/', methods=['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        cursor.execute('SELECT * FROM userdetails WHERE username=%s AND password=%s', (username, password))
        record = cursor.fetchall()
        if record:
            session['loggedin'] = True
            session['username'] = record[5]
            return "Welcome"
        else:
            msg = 'Incorrect Username/Password'

    return render_template('login.html', msg = msg)
  
  @app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name')
        dob = request.form.get('dob')
        email = request.form.get('email')
        username = request.form.get('username')
        password = request.form.get('password')

        entry = Userdetails(Name = name, DOB = dob, Email = email, Username = username, Password = password, Date = datetime.now())
        db.session.add(entry)
        db.session.commit()


        return redirect('/')
    return render_template('register.html')


if __name__ == '__main__':
    app.run(debug = True)
