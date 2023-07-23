from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
import pyrebase

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'super-secret-key'


config = {
  "apiKey": "AIzaSyDB9y26xcCgxl4E3gbFkaD935bE43rmx4g",
  "authDomain": "rogalachem.firebaseapp.com",
  "projectId": "rogalachem",
  "storageBucket": "rogalachem.appspot.com",
  "messagingSenderId": "286426368528",
  "appId": "1:286426368528:web:6a67e87b9cd50f3eaf5895",
  "measurementId": "G-SWDS6VP6GH",
  "databaseURL": ""
}

@app.route('/', methods=['GET', 'POST'])
def signin():
    error = ""
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try:
            login_session['user'] = auth.sign_in_with_email_and_password(email, password)
            return redirect(url_for('home'))
        except:
            error = "Authentication failed"
            return render_template("signin.html")


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    error = ""
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try:
            login_session['user'] = auth.create_user_with_email_and_password(email, password)
            return redirect(url_for('home'))
        except:
            error = "Authentication failed"
            return render_template("signup.html")


@app.route('/add_tweet', methods=['GET', 'POST'])
def add_tweet():
    return render_template("add_tweet.html")


firebase = pyrebase.initialize_app(config)
auth = firebase.auth()


if __name__ == '__main__':
    app.run(debug=True)