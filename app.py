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
        email = request.form["email"]
        password = request.form["password"]
        confirm_password = request.form["confirm_password"]
        if password == confirm_password:
            try:
                login_session['user'] = auth.create_user_with_email_and_password(email, password)
                return redirect(url_for('signin'))
            except:
                return redirect(url_for('signin', error = "Authentication failed"))
        else:
            return redirect(url_for('signup', error = "Confirm password does not match"))
    return render_template("signup.html")

@app.route('/he_signin', methods=['GET', 'POST'])
def hesignin():
    error = ""
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try:
            login_session['user'] = auth.sign_in_with_email_and_password(email, password)
            return redirect(url_for('home'))
        except:
            error = "Authentication failed"
    return render_template("he_signin.html")

@app.route('/ar_signin', methods=['GET', 'POST'])
def arsignin():
    error = ""
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try:
            login_session['user'] = auth.sign_in_with_email_and_password(email, password)
            return redirect(url_for('home'))
        except:
            error = "Authentication failed"
    return render_template("ar_signin.html")

@app.route('/he_signup', methods=['GET', 'POST'])
def hesignup():
    error = ""
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try:
            login_session['user'] = auth.create_user_with_email_and_password(email, password)
            return redirect(url_for('hesignin'))
        except:
            error = "Authentication failed"
    return render_template("he_signup.html")

@app.route('/ar_signup', methods=['GET', 'POST'])
def arsignup():
    error = ""
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try:
            login_session['user'] = auth.create_user_with_email_and_password(email, password)
            return redirect(url_for('arsignin'))
        except:
            error = "Authentication failed"
            return render_template("ar_signup.html", error = error)
    return render_template("ar_signup.html", error = error)

@app.route('/admin', methods=['GET', 'POST'])
def admin():
        
  if request.method == 'POST':
    name = request.form["name"]
    humidity = request.form["humidity"]
    sunlight = request.form["sunlight"]
    try:
      post = {"name" : name, "humidity" : humidity, "sunlight": sunlight , "uid":login_session['user']['localId']}
      db.child("posts").push(post)
      return redirect(url_for('home'))
    except:
      error = "Authentication failed"
  return render_template("admin.html")

@app.route('/show_info/<string:plant_id>', methods=['GET', 'POST'])
def showinfo(plant_id):
  post = db.child("posts").get().val()
  return render_template("show_info.html", t = post, pid=plant_id)

@app.route('/home')
def home():
    return render_template('home.html')

if __name__ == '__main__':
    app.run(debug=True)
