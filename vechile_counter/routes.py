from flask import Flask, render_template, Response
from vechile_counter.ardi_utils import car_counting
from vechile_counter import app, mysql


@app.route("/video_feed", methods=['GET'])
def video_feed():
    global car_down, car_up, global_frame, readAbleCar
    
    readAbleCar = None 
    v = car_counting.vechile()
    return Response(v.vechile_counting(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/')
def index():
    cur = mysql.connection.cursor()
    # cur.execute("INSERT INTO tbl_kendaraan(lokasi,jml_kendaraan) VALUES (%s, %s)", "Tangerang", str(car))
    # mysql.connection.commit()

    return render_template('index.html')
