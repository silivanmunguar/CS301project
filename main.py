from flask import Flask, render_template, request, url_for, redirect, flash, session
import bcrypt, random
import cs304dbi as dbi
from werkzeug.utils import secure_filename
import os

dbi.conf(db='alikadk_db')


UPLOAD_FOLDER = '~alikadk/cs301db/homework/hw5/ven/project/CS301project/uploads'
ALLOWED_EXTENSIONS = { 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


app.secret_key = ''.join([random.choice(('ABCDEFGHIJKLMNOPQRSTUVXYZ' + 
                                         'abcdefghijklmnopqrstuvxyz' +
                                         '0123456789'))
                          for i in range(20)])

@app.route("/")
def home():
    if 'logged_in' in session:
        is_logged_in = session['logged_in']
        if is_logged_in:
            return redirect(url_for('events'))
        return render_template("landingPage.html")
    return render_template("landingPage.html")

@app.route("/home")
def home():
   return render_template("landingPage.html")
 
# Pull events from db and pass them onto html
@app.route("/events")
def events():
    if 'email' in session:
        conn = dbi.connect()
        curs = dbi.cursor(conn)
        curs.execute("SELECT * FROM Events;")
        results = curs.fetchall()
        print(results)
        return render_template('myEvent.html', events=results)
    flash("You are not logged in")
    return redirect(url_for('home'))

@app.route("/createEvent", methods=["GET", "POST"])
def createEvents():
    if request.method == "GET":
        return render_template("eventForm.html")
    else:
        try:
            eventName= request.form["eventName"]
            location= request.form["location"]
            time= request.form['eventTime']
            description =request.form['description']
            if request.files['file'].filename != '':
                print('hi')
                filename = secure_filename(request.files['file'].filename)
                request.files['file'].save(filename)
            con= dbi.connect()
            crs= dbi.cursor(con)
            query2=f" insert into Events values (NULL, '{eventName}', '{description}', '{time}', '{location}', {session['stuid']});" 
            print(query2)
            crs.execute(query2)
            con.commit()
            flash("Event added")
            return render_template('eventForm.html')
        except Exception as err:
            flash(f"form submission error {err}.\n Please try again!")
            return render_template('eventForm.html')


@app.route("/logout")
def logout():
    try:
        session.pop('stuid', None)
        session.pop('email', None)
        session.pop('logged_in', None)
        session.pop('name', None)
        flash("you have logged out")
    except Exception as err:
        flash(f"error {error}")
    
    return render_template("landingPage.html")

@app.route("/my-event")
def myEvent():
    if 'email' in session: #'email' in session:
        conn = dbi.connect()
        curs = dbi.cursor(conn)
        curs.execute("SELECT * FROM Events;")
        allEvents = curs.fetchall()
        print(allEvents)
        return render_template('myEvent.html', allEvents=allEvents)
    flash("You are not logged in")
    return redirect(url_for('home'))



@app.route("/log-in", methods=["POST"])
def login():
    try:
        email = request.form["email"]
        password = request.form["password"]
        conn = dbi.connect()
        curs = dbi.dict_cursor(conn)
        curs.execute('''SELECT *
                      FROM Users
                      WHERE email = %s''',
                     [email])
        row = curs.fetchone()
        if row is None:
            flash('Email or password is incorrectNULL. Try again or sign up.')
            return redirect(url_for('home'))

        hashed_db = row["hashed_pwd"]
        hashed_user = bcrypt.hashpw(password.encode(), hashed_db.encode())
        print(f"hashed db is {hashed_db}. Hashed user is {hashed_user}.")
        print(hashed_user == hashed_db.encode())
        if hashed_user == hashed_db.encode():
            flash('Successfully logged in.')
            name = row['name']
            session['name'] = name
            session['email'] = email
            session['stuid'] = row['stuid']
            session['logged_in'] = True 
            return render_template('event.html', name = name)
        else:
            flash('Email or password is incorrect. Try again or sign up.')
            return redirect(url_for('home'))
    except Exception as err:
        flash(f"form submission error {err}")
        return "error"  

@app.route("/sign-up", methods=["POST"])
def signup():
    try:
        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]
        hashed = bcrypt.hashpw(password.encode('UTF-8'), bcrypt.gensalt())

        print(f"the password is {password}, The hashed password is {hashed}")

        dbi.conf(db='lect_db')
        conn = dbi.connect()
        curs = dbi.cursor(conn)
        try:
            curs.execute('''INSERT INTO Users(name,email,hashed_pwd)
                            VALUES(%s,%s, %s)''',
                        [name, email, hashed])
            conn.commit()
        except Exception as err:
            flash(f'The email {email} is already associated with another account')
            return redirect(url_for('home'))

        curs.execute('SELECT last_insert_id()')
        row = curs.fetchone()
        stuid = row[0]
        
        flash(f"Successfully signed up!")
        return redirect(url_for('home'))
    except Exception as err:
        flash(f"form submission error {err}")
        print(err)
        return "error"

if __name__ == "__main__":
    #dbi.cache_cnf()   # defaults to ~/.my.cnf
    app.run(debug=True, port=5000)


