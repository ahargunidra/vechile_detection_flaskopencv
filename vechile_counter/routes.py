from flask import Flask, render_template, Response
from vechile_counter.ardi_utils import car_counting
from vechile_counter import app, mysql


@app.route("/video_feed", methods=['GET'])
def video_feed():

    """Video streaming route. Put this in the src attribute of an img tag."""
    global car, global_frame
    v = car_counting.vechile()
    return Response(v.vechile_counting(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/')
def index():
    return render_template('index.html')
