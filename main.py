from flask import Flask, render_template, request, url_for, redirect, flash, session
import bcrypt, random
import cs304dbi as dbi

app = Flask(__name__)

app.secret_key = ''.join([random.choice(('ABCDEFGHIJKLMNOPQRSTUVXYZ' + 
                                         'abcdefghijklmnopqrstuvxyz' +
                                         '0123456789'))
                          for i in range(20)])

@app.route("/")
def index():
    return "Bonjour Emily"

@app.route("/home")
def home():
    return render_template("landingPage.html")


@app.route("/createEvent", methods=["GET", "POST"])
def createEvents():

    session['stuid']=0
    if request.method == "GET":
        #return 'hello mfers'
        return render_template("eventForm.html")
    else:
        try:
            eventName= request.form["eventName"]
            location= request.form["location"]
            time= request.form['eventTime']
            description =request.form['description']
            dbi.conf(db='alikadk_db')
            con= dbi.connect()
            crs= dbi.dict_cursor(con)
            q="select * from Events;"
            query=f"set @lid := select last_insert_id() from Events; insert into Events values (select lid+1, {eventName}, {descrip}, {time}, {location}); insert into CreatedBy values (select lid+1, {session['stuid']});"
            crs.execute(query)
            con.commit()
            return render_template("landingpage.html")
        except Exception as err:
            flash(f"form submission error {err}")
            return render_template("landingPage.html")
            #return render_template('eventForm.html')

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
        return render_template("logged-in.html", email=email, password=password)
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

