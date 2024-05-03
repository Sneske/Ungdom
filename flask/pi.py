#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
import os
path = "//home/pi/Documents/ungdom/Test/pic"

from waveshare_epd import epd2in7
from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import logging


import time
from PIL import Image,ImageDraw,ImageFont
import traceback
from gpiozero import LED, Button
from signal import pause

currentDay = sys.argv[1]
selectDay = sys.argv[2]
nextDay = sys.argv[3]
lastDay = sys.argv[4]

#currentTime = sys.argv[5] 
#selectTime = sys.argv[6]
#dayScroll = sys.argv[7]
#logging.basicConfig(level=logging.DEBUG)
currentTime = 13 
selectTime = currentTime

days = sys.argv[5]

on = True
days = {1: [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0]}, {2: [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0]}, {3: [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0]}, {4: [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0]}, {5: [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0]}, {6: [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0]}, {7: [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0]}, {8: [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 
0, 1, 0, 1, 0, 1, 0, 1, 0]}, {9: [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0]}, {10: [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0]}, {11: [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0]}, {12: [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0]}, {13: [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0]}, {14: [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0]}, {15: [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0]}, {16: [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0]}, {17: [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0]}, {18: [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0]}, {19: [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0]}, {20: [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0]}, {21: [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0]}, {22: [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0]}, {23: [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 
1, 0, 1, 0, 1, 0]}, {24: [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0]}, {25: [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0]}, {26: [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0]}, {27: [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 
1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0]}, {28: [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0]}, {29: [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0]}, {30: [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0]}, {31: [1, 0, 1, 0, 1, 0, 
1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0]}



currentDay = 5
selectDay = currentDay
nextDay = currentDay +1
lastDay = currentDay -1

key1 = Button(5)
key2 = Button(6)
key3 = Button(13)
key4 = Button(19)




database = os.getcwd() + '/events.db'
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{database}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Event(db.Model):
    __tablename__ = 'event'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    start = db.Column(db.DateTime, nullable=False)
    end = db.Column(db.DateTime, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'start': self.start.isoformat(),
            'end': self.end.isoformat()
        }

  




def run(currentDay,selectDay,nextDay,lastDay,currentTime,selectTime,days):
    epd = epd2in7.EPD()
    epd.init()
    epd.Clear(0xFF)
    font12 = ImageFont.truetype(os.path.join(path, 'Font.ttc'), 12)
    Himage = Image.new('1', (epd.height, epd.width), 255)
    draw = ImageDraw.Draw(Himage)
    def line(x,y,xp,yp,fill):
        return draw.line((x, y, x+xp, y+yp), fill = fill)
    def react(x,y,xp,yp,fill,fillType):
        if fillType == 0:
            return draw.rectangle((x, y, x+xp, y+yp ), outline = fill)
        else: 
            return draw.rectangle((x, y, x+xp, y+yp), fill = fill)
    def text(x,y,font,fill,text):
        draw.text((x, y), text, font = font, fill = fill)
    nextDay = currentDay +1
    lastDay = currentDay -1
    react(0,136,264,40,0,255)
    line(88, 176, 0, -176, 0)
    line(174, 176, 0, -176, 0)
    text(176,136,font12,255,str(nextDay)+"April")    
    text(90,136,font12,255,str(selectDay)+"April")
    text(2,136,font12,255,str(lastDay)+"April")
    for i in range(8):
        line(0 , 17*i , 264 , 0,0)
    
    for i in range(3):
        react(22+i*86,0,65,136,255,1)

    react(194,0,68,136,255,1)
    for i in range(8):
        for x in range(3):
            if 0 <= x+selectDay < len(days) and 0 <= selectTime-4+i < len(days[x+selectDay]):
                if days[x+selectDay][selectTime-4+i] == 1:
                    react(x*88,i*17,88,17,0,1) 
                    text(2+x*88,3+i*17,font12,255,str(selectTime-4+i)+":00")
                else:
                    text(2+x*88,3+i*17,font12,0,str(selectTime-4+i)+":00")
            else:
                print(len(days))
                print(len(days[x+selectDay]))
                print(x+selectDay)
                print(selectTime-4+i)
                print("fuck")
                pass

    epd.display(epd.getbuffer(Himage))



try:
    run(currentDay,selectDay,nextDay,lastDay,currentTime,selectTime,days)
    while on:
        if key1.is_pressed == True:
            selectTime -= 1
            run(currentDay,selectDay,nextDay,lastDay,currentTime,selectTime,days)

            time.sleep(0.5)
        if key2.is_pressed == True:
            selectTime += 1
            print("kage")
            run(currentDay,selectDay,nextDay,lastDay,currentTime,selectTime,days)
            time.sleep(0.5)

        if key3.is_pressed == True:
            selectDay += 1
            print("pik")
            run(currentDay,selectDay,nextDay,lastDay,currentTime,selectTime,days)
            time.sleep(0.5) 
        
        if key4.is_pressed == True:
            print("homo")
            selectDay -= 1 
            run(currentDay,selectDay,nextDay,lastDay,currentTime,selectTime,days)
            time.sleep(0.5)
    
    
except KeyboardInterrupt:    
    logging.info("ctrl + c:")
    epd2in7.epdconfig.module_exit(cleanup=True)
    exit()





