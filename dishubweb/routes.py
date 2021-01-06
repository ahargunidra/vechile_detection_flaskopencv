from flask import render_template, url_for, Response, flash, redirect, request, abort, session
from dishubweb import app, mysql
from flask_mysqldb import MySQLdb
import bcrypt
from dishubweb.cameraArdi import VideoCamera
import cv2

@app.route('/')
@app.route('/home')
def home():
    return render_template('layout.html')

@app.route('/test')
def test():
    return render_template('index.html')

def gen():
    """Video streaming generator function."""
    cap = cv2.VideoCapture('drone.mp4')

    # Read until video is completed
    while(cap.isOpened()):
    # Capture frame-by-frame
        ret, img = cap.read()
        if ret == True:
            img = cv2.resize(img, (0,0), fx=0.5, fy=0.5) 
            frame = cv2.imencode('.jpg', img)[1].tobytes()
            yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            time.sleep(0.1)
        else: 
            break
        

@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')
#@app.route('/register', methods=["GET", "POST"])
# def register():
#     if request.method == 'GET':
#         return render_template('register.html')
#     else:
#         name = request.form['name']
#         email = request.form['email']
#         password = request.form['password'].encode('utf-8')
#         hash_password = bcrypt.hashpw(password, bcrypt.gensalt())

#         cur = mysql.connection.cursor()
#         cur.execute("INSERT INTO tbl_user (name, email, password) VALUES (%s,%s,%s)",
#         (name,email,hash_password))
#         mysql.connection.commit()
#         session['name'] = request.form['name']
#         session['email'] = request.form['email']
#         return redirect(url_for('home'))

# @app.route('/logout')
# def logout():
#     session.clear()
#     return render_template('login.html')

# @app.route('/login', methods=["GET","POST"])
# def login():
#     if request.method == 'POST':
#         email = request.form['email']
#         password = request.form['password'].encode('utf-8')
#         curl = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
#         curl.execute("SELECT * FROM tbl_user WHERE email = %s", (email,))
#         user = curl.fetchone()
#         curl.close()
#         if len(user) > 1:
#             if bcrypt.hashpw(password, user['password'].encode('utf-8')) == user['password'].encode('utf-8'):
#                 session['name'] = user['name']
#                 session['email'] = user['email']
#                 return render_template('home.html')
#             else:
#                 return "Password/Username salah"
#         else:
#             return 'User tidak di temukan'
#     else: 
#         return render_template("login.html")

