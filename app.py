from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
import pyrebase

config = {
  "apiKey": "AIzaSyDH5JZXMLJ7QRw6uieGusMjSSasHL2X294",
  "authDomain": "finalproject-c86cf.firebaseapp.com",
  "projectId": "finalproject-c86cf",
  "storageBucket": "finalproject-c86cf.appspot.com",
  "messagingSenderId": "934737561719",
  "appId": "1:934737561719:web:1e3cebf29898181e159e72",
  "measurementId": "G-Q27510YY60",
  "databaseURL": "https://finalproject-c86cf-default-rtdb.europe-west1.firebasedatabase.app/"
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()


app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'super-secret-key'

@app.route('/')
def home():
    return render_template("home.html")


@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try:
            login_session['user'] = auth.sign_in_with_email_and_password(email, password)
            login_session['more_info'] = db.child('Users').child(login_session['user']['localId']).get().val()
            for i in db.child('Survey').get().val():
                if db.child('Survey').child(i).get().val()["uid"] == login_session['user']['localId']:
                    db_users_survey = db.child('Survey').child(i).get().val()
                    login_session['survey'] = {"animal":db_users_survey['animal'],"color":db_users_survey['color'],"food":db_users_survey['food'],"hobby":db_users_survey['hobby'],"city":db_users_survey['city'],"place":db_users_survey['place'],"drink":db_users_survey['drink'],"subject":db_users_survey['subject']}
            return redirect(url_for('add_tweet'))
        except:
            error = "Authentication failed"
    return render_template("signin.html")


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        #try:
        user_value = request.form['username']
        for i in db.child("Users").get().val():
            if db.child("Users").child(i).get().val()['username'] == user_value:
                raise TypeError("User already exists")

        login_session['user'] = auth.create_user_with_email_and_password(email, password)
        user = {"fullname": request.form['fullname'], "username" :user_value, "bio":request.form['bio']}
        login_session['more_info'] = user
        db.child("Users").child(login_session['user']['localId']).set(user)
        return redirect(url_for("survey"))
        #except:
        #    error = "Authentication failed"
    return render_template("signup.html")


@app.route('/add_tweet', methods=['GET', 'POST'])
def add_tweet():
    if request.method == 'POST':
        quote = {"quote":request.form['quote']}
        quote["uid"] = login_session['user']['localId']
        db.child("Quotes").push(quote)

        return redirect(url_for("all_tweets"))
    return render_template("add_tweet.html")

@app.route('/all_tweets')
def all_tweets():
    quote_db = db.child("Quotes").get().val()
    return render_template("tweets.html", databis = db, quote_db=quote_db)


@app.route('/signout')
def signout():
    login_session = {}
    auth.current_user = None
    return redirect(url_for('home'))


@app.route('/survey', methods=['GET', 'POST'])
def survey():
    if request.method == 'POST':
        survey1 = {"animal":request.form['animal'].lower(),"color":request.form['color'].lower(),"food":request.form['food'].lower(),"hobby":request.form['hobby'].lower(),"city":request.form['city'].lower(),"place":request.form['place'].lower(),"drink":request.form['drink'].lower(),"subject":request.form['subject'].lower()}
        survey1["uid"] = login_session['user']['localId']
        login_session['survey'] = survey1
        db.child("Survey").push(survey1)
        return redirect(url_for("add_tweet"))
    return render_template("survey.html")

@app.route('/sameinfo/<string:name>')
def sameinfo(name):
    login_session_user = login_session['more_info']
    login_session_survey = login_session['survey']
    return render_template('sameinfo.html', n = name, login_session_user = login_session_user, databis = db, login_session_survey = login_session_survey)



if __name__ == '__main__':
    app.run(debug=True)