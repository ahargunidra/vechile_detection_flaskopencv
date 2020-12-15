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
from vechile_counter import app, mysql

rectangle_min = 80
altura_min = 80
offset = 6
pos_line = 550
delay = 60  # FPS
detec = []
car = 0
global_frame = None


class vechile():
    def center_pick(self,x, y, width, height):
        x1 = width // 2
        y1 = height // 2
        cx = x + x1
        cy = y + y1
        return cx, cy
        
    def set_info(self,detec):
        global car, global_frame
        f = open("Data.txt", "w")
        # print("THIS IS CUR :", cur)
        for (x, y) in detec:
            if (pos_line + offset) > y > (pos_line - offset):
                car += 1
                cv2.line(global_frame, (25, pos_line), (1200, pos_line), (0, 127, 255), 3)
                detec.remove((x, y))
                print("Car detection: " + str(car))
        f.write("DATA KENDARAAN : " + str(car))
        # cur.execute("INSERT INTO tbl_kendaraan(lokasi,jml_kendaraan) VALUES (%s, %s)", "Tangerang", str(car))
        # mysql.connection.commit()
        f.close()
        # cursor.close()
    def show_info(self, frame1, dilated):
        global car
        text = f'Car: {car}'
        cv2.putText(frame1, text, (450, 70), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 5)

    def vechile_counting(self):
        car = caminhoes = 0
        cap = cv2.VideoCapture('vechile_counter/video1.mp4')
        subtract = cv2.bgsegm.createBackgroundSubtractorMOG()  # Take the bottom and subtract from what's moving
        while True:
            ret, frame1 = cap.read()  # Takes each frame of the video
            global global_frame # Global var for passing parameters
            global_frame = frame1
            tempo = float(1 / delay)
            sleep(tempo)  # Gives a delay between each processing
            grey = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)  # Takes the frame and turns to black and white
            blur = cv2.GaussianBlur(grey, (3, 3), 5)  # Faz um blur para tentar remover as imperfeições da imagem
            img_sub = subtract.apply(blur)  # Faz a subtração da imagem aplicada no blur
            dilat = cv2.dilate(img_sub, np.ones((5, 5)))  # "Engrossa" o que sobrou da subtração
            kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (
                5, 5))  # Cria uma matriz 5x5, em que o formato da matriz entre 0 e 1 forma uma elipse dentro
            dilated = cv2.morphologyEx(dilat, cv2.MORPH_CLOSE, kernel)  # Tenta preencher todos os "buracos" da imagem
            dilated = cv2.morphologyEx(dilated, cv2.MORPH_CLOSE, kernel)

            contour, img = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            cv2.line(frame1, (25, pos_line), (1200, pos_line), (255, 127, 0), 3)
            for (i, c) in enumerate(contour):
                (x, y, w, h) = cv2.boundingRect(c)
                validar_contorno = (w >= rectangle_min) and (h >= altura_min)
                if not validar_contorno:
                    continue
                cv2.rectangle(frame1, (x, y), (x + w, y + h), (0, 255, 0), 2)
                center = self.center_pick(x, y, w, h)
                detec.append(center)
                cv2.circle(frame1, center, 4, (0, 0, 255), -1)
            self.set_info(detec)
            self.show_info(frame1, dilated)
            if cv2.waitKey(1) == 27:
                break
            frame = cv2.imencode('.jpg', frame1)[1].tobytes()
            yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


