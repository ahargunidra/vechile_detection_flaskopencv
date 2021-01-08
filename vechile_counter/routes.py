from flask import Flask, render_template, Response, request, session, redirect,url_for,flash
from vechile_counter.ardi_utils import car_counting
from vechile_counter import app, mysql
import bcrypt
from flask_mysqldb import MySQLdb
import MySQLdb

@app.route("/video_feed", methods=['GET'])
def video_feed():
    carDown = car_counting.car_down
    v = car_counting.vechile()
    return Response(v.vechile_counting(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/')
def index():
    carDown = car_counting.car_down
    carUp = car_counting.car_up
    return render_template('index.html', car_down=carDown, car_up=carUp)

@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    elif request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password'].encode('utf-8')
        hash_password = bcrypt.hashpw(password, bcrypt.gensalt())

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO tbl_user (name, email, password) VALUES (%s,%s,%s)",
        (name,email,hash_password))
        mysql.connection.commit()
        session['name'] = request.form['name']
        session['email'] = request.form['email']
        return redirect(url_for('login'))

@app.route('/login', methods=["GET","POST"])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password'].encode('utf-8')
        curl = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        curl.execute("SELECT * FROM tbl_user WHERE email = %s", (email,))
        user = curl.fetchone()
        curl.close()
        print("EMAIL : ", email)
        print("PASS : ", password)
        print("USER : ", user)
        if user != None :
            if bcrypt.hashpw(password, user['password'].encode('utf-8')) == user['password'].encode('utf-8'):
                session['name'] = user['name']
                session['email'] = user['email']
                return render_template('index.html')
            else:
                return "Password/Username salah"
        else:
            return "User tidak di temukan"
    else:
        return render_template("login.html")

# @app.route('/logout')
# def logout():
#     session.clear()
#     return render_template('login.html')