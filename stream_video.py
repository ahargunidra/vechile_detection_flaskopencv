# -*- coding: utf-8 -*-
"""
"""
import time
import cv2 
import numpy as np
from flask import Flask, render_template, Response
from pyimagesearch.centroidtracker import CentroidTracker
from pyimagesearch.trackableobject import TrackableObject
from imutils.video import VideoStream
from imutils.video import FPS
import argparse
import imutils
import time
import dlib
from time import sleep

largura_min = 80  # Largura minima do retangulo
altura_min = 80  # Altura minima do retangulo
offset = 6  # Erro permitido entre pixel
pos_linha = 550  # Posição da linha de contagem
delay = 60  # FPS do vídeo
detec = []
carros = 0
app = Flask(__name__)

@app.route('/')
def index():
    """Video streaming home page."""
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

def people_counter():
    cap = cv2.VideoCapture("768x576.avi")
    frames_count, fps, width, height = cap.get(cv2.CAP_PROP_FRAME_COUNT), cap.get(cv2.CAP_PROP_FPS), cap.get(
        cv2.CAP_PROP_FRAME_WIDTH), cap.get(cv2.CAP_PROP_FRAME_HEIGHT)

    width = int(width)
    height = int(height)
    print(frames_count, fps, width, height)


    sub = cv2.createBackgroundSubtractorMOG2()  # create background subtractor
    ret, frame = cap.read()  # import image
    ratio = 1.0
    while True:
        ret, frame = cap.read()  # import image
        if not ret: #if vid finish repeat
            frame = cv2.VideoCapture("768x576.avi")
            continue
        if ret:  # if there is a frame continue with code
            image = cv2.resize(frame, (0, 0), None, ratio, ratio)  # resize image
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # converts image to gray
            fgmask = sub.apply(gray)  # uses the background subtraction
            kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))  # kernel to apply to the morphology
            closing = cv2.morphologyEx(fgmask, cv2.MORPH_CLOSE, kernel)
            opening = cv2.morphologyEx(closing, cv2.MORPH_OPEN, kernel)
            dilation = cv2.dilate(opening, kernel)
            retvalbin, bins = cv2.threshold(dilation, 220, 255, cv2.THRESH_BINARY)  # removes the shadows
            contours, hierarchy = cv2.findContours(dilation, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            minarea = 400
            maxarea = 50000
            cxx = np.zeros(len(contours))
            cyy = np.zeros(len(contours)) 
            for i in range(len(contours)):  # cycles through all contours in current frame
                if hierarchy[0, i, 3] == -1:  # using hierarchy to only count parent contours (contours not within others)
                    area = cv2.contourArea(contours[i])  # area of contour
                    if minarea < area < maxarea:  # area threshold for contour
                        # calculating centroids of contours
                        cnt = contours[i]
                        M = cv2.moments(cnt)
                        cx = int(M['m10'] / M['m00'])
                        cy = int(M['m01'] / M['m00'])
                        # gets bounding points of contour to create rectangle
                        # x,y is top left corner and w,h is width and height
                        x, y, w, h = cv2.boundingRect(cnt)
                        # creates a rectangle around contour
                        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
                        # Prints centroid text in order to double check later on
                        cv2.putText(image, str(cx) + "," + str(cy), (cx + 10, cy + 10), cv2.FONT_HERSHEY_SIMPLEX,.3, (0, 0, 255), 1)
                        cv2.drawMarker(image, (cx, cy), (0, 255, 255), cv2.MARKER_CROSS, markerSize=8, thickness=3,line_type=cv2.LINE_8)
        # cv2.imshow("countours", image)
        frame = cv2.imencode('.jpg', image)[1].tobytes()
        yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        time.sleep(0.1)
        key = cv2.waitKey(20)
        if key == 27:
            break

def vechile_counting():
    def pega_centro(x, y, largura, altura):
        """
        :param x: x do objeto
        :param y: y do objeto
        :param largura: largura do objeto
        :param altura: altura do objeto
        :return: tupla que contém as coordenadas do centro de um objeto
        """
        x1 = largura // 2
        y1 = altura // 2
        cx = x + x1
        cy = y + y1
        return cx, cy

    def set_info(detec):
        global carros
        for (x, y) in detec:
            if (pos_linha + offset) > y > (pos_linha - offset):
                carros += 1
                cv2.line(frame1, (25, pos_linha), (1200, pos_linha), (0, 127, 255), 3)
                detec.remove((x, y))
                print("Carros detectados até o momento: " + str(carros))


    def show_info(frame1, dilatada):
        global carros
        text = f'Car: {carros}'
        cv2.putText(frame1, text, (450, 70), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 5)

    carros = caminhoes = 0
    cap = cv2.VideoCapture('video.mp4')
    subtracao = cv2.bgsegm.createBackgroundSubtractorMOG()  # Pega o fundo e subtrai do que está se movendo

    while True:
        ret, frame1 = cap.read()  # Pega cada frame do vídeo
        tempo = float(1 / delay)
        sleep(tempo)  # Dá um delay entre cada processamento
        grey = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)  # Pega o frame e transforma para preto e branco
        blur = cv2.GaussianBlur(grey, (3, 3), 5)  # Faz um blur para tentar remover as imperfeições da imagem
        img_sub = subtracao.apply(blur)  # Faz a subtração da imagem aplicada no blur
        dilat = cv2.dilate(img_sub, np.ones((5, 5)))  # "Engrossa" o que sobrou da subtração
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (
            5, 5))  # Cria uma matriz 5x5, em que o formato da matriz entre 0 e 1 forma uma elipse dentro
        dilatada = cv2.morphologyEx(dilat, cv2.MORPH_CLOSE, kernel)  # Tenta preencher todos os "buracos" da imagem
        dilatada = cv2.morphologyEx(dilatada, cv2.MORPH_CLOSE, kernel)

        contorno, img = cv2.findContours(dilatada, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        cv2.line(frame1, (25, pos_linha), (1200, pos_linha), (255, 127, 0), 3)
        for (i, c) in enumerate(contorno):
            (x, y, w, h) = cv2.boundingRect(c)
            validar_contorno = (w >= largura_min) and (h >= altura_min)
            if not validar_contorno:
                continue

            cv2.rectangle(frame1, (x, y), (x + w, y + h), (0, 255, 0), 2)
            centro = pega_centro(x, y, w, h)
            detec.append(centro)
            cv2.circle(frame1, centro, 4, (0, 0, 255), -1)

        set_info(detec)
        show_info(frame1, dilatada)
        if cv2.waitKey(1) == 27:
            break
        frame = cv2.imencode('.jpg', frame1)[1].tobytes()
        yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(vechile_counting(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

    
if __name__ == "__main__":
    debug(True)
