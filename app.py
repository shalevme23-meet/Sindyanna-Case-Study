from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
import pyrebase

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'super-secret-key'

config = {
      "apiKey": "AIzaSyDfTr0-f99pBlrgPIjXBbCXomYPwD4s5jc",
      "authDomain": "sindyanna-meet.firebaseapp.com",
      "databaseURL": "https://sindyanna-meet-default-rtdb.firebaseio.com",
      "projectId": "sindyanna-meet",
      "storageBucket": "sindyanna-meet.appspot.com",
      "messagingSenderId": "658775746831",
      "appId": "1:658775746831:web:70bb5d0785ad4c4a5c767a",
      "measurementId": "G-3HN7C637P4"
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()

@app.route('/', methods=['GET', 'POST'])
def signup():
  error = ""
  if request.method == 'POST':
    email = request.form['email']
    password = request.form['password']
    try:
      login_session['user'] = auth.create_user_with_email_and_password(email, password)
      return redirect(url_for('signup'))
    except:
      error = "Authentication failed"
  return render_template("signin.html")

  

if __name__ == '__main__':
    app.run(debug=True)