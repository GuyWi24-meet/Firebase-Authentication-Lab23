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
  "databaseURL": "https://rogalachem-default-rtdb.europe-west1.firebasedatabase.app/"
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
# ... (existing code)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    error = ""
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        username = request.form['username']
        Bio = request.form['Bio']

        try:
            user = auth.create_user_with_email_and_password(email, password)

            user_data = {
                'email': email,
                'password': password,
                'username': username,
                'Bio': Bio
            }

            db.child("Users").child(user['localId']).set(user_data)

            login_session['user'] = user
            return redirect(url_for('home'))
        except Exception as e:
            error = "Authentication failed: " + str(e)

    return render_template("signup.html", error=error)

@app.route('/add_tweet', methods=['GET', 'POST'])
def add_tweet():
    if request.method == 'POST':
        title = request.form['title']
        text = request.form['text']

        if 'user' in login_session:
            user_uid = login_session['user']['localId']

            tweet = {
                'title': title,
                'text': text,
                'uid': user_uid
            }

            try:
                db.child("Tweets").push(tweet)
                return redirect(url_for('home'))
            except Exception as e:
                print("Error adding tweet to the database:", str(e))
        
    return render_template("add_tweet.html")

@app.route('/all_tweets')
def all_tweets():
    try:
        tweets = db.child("Tweets").get().val()
        return render_template("tweets.html", tweets=tweets)
    except Exception as e:
        print("Error retrieving tweets from the database:", str(e))

    return "Error: Unable to retrieve tweets."


firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()

if __name__ == '__main__':
    app.run(debug=True)