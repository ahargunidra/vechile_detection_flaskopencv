import time
import cv2 
import numpy as np
from flask import Flask, render_template, Response
from imutils.video import VideoStream
from imutils.video import FPS
import argparse
import imutils
import time
import dlib
from time import sleep
from ardi_utils import car_counting

app = Flask(__name__)

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


if __name__ == "__main__":
    app.run(debug=True)
