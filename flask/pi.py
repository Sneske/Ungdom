#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
import os
path = "//home/pi/Documents/ungdom/Test/pic"

import logging
from waveshare_epd import epd2in7
import time
from PIL import Image,ImageDraw,ImageFont
import traceback
from gpiozero import LED, Button
from signal import pause
from gpiozero import Button
currentDay = "currentDay"
selectDay = "selectDay"
nextDay = "nextDay"
lastDay = "lastDay"
currentTime = 12 
selectTime = 11
dayScroll = 0
#logging.basicConfig(level=logging.DEBUG)
on = True
days = {1:[1,0,0,1,0,0,1,0,1,0,1,1,0,1,0,0,1,0,0,1,0,1,0,1,1,0,1,0,0,1,0,0,1,0,1,0,1,1,0],2:[1,0,0,1,0,0,0,1,0,0,1,0,0,0,1,0,0,1,0,0,0,1,0,0,1,0,0,0,1,0,0,1,0,0,0,1,0,0,1,0,0,0,1],3:[1,0,0,1,0,0,0,1,0,0,1,0,0,0,1,0,0,1,0,0,0,1,0,0,1,0,0,0,1,0,0,1,0,0,0,1,0,0,1,0,0,0,1]}

key1 = Button(5)
key2 = Button(6)
key3 = Button(13)
key4 = Button(19)
def run(currentDay,selectDay,nextDay,lastDay,currentTime,selectTime,dayScroll,days):


    def line(x,y,xp,yp,fill):
        return draw.line((x, y, x+xp, y+yp), fill = fill)

    def react(x,y,xp,yp,fill,fillType):

        if fillType == 0:
            return draw.rectangle((x, y, x+xp, y+yp ), outline = fill)
        else: 
            return draw.rectangle((x, y, x+xp, y+yp), fill = fill)


    def text(x,y,font,fill,text):
        draw.text((x, y), text, font = font, fill = fill)

    #logging.info("epd2in7 Demo")   
    epd = epd2in7.EPD()
    #'''2Gray(Black and white) display'''
    #logging.info("init and Clear")
    epd.init()
    epd.Clear(0xFF)
    font24 = ImageFont.truetype(os.path.join(path, 'Font.ttc'), 24)
    font18 = ImageFont.truetype(os.path.join(path, 'Font.ttc'), 18)
    font35 = ImageFont.truetype(os.path.join(path, 'Font.ttc'), 35)
    font12 = ImageFont.truetype(os.path.join(path, 'Font.ttc'), 12)
    #Drawing on the Horizontal image
    #logging.info("1.Drawing on the Horizontal image...")
    Himage = Image.new('1', (epd.height, epd.width), 255)  # 255: clear the frame
    draw = ImageDraw.Draw(Himage)
    react(0,136,264,40,0,255)
    line(88, 176, 0, -176, 0)
    line(174, 176, 0, -176, 0)

   
    text(176,136,font12,255,nextDay)    
    text(90,136,font12,255,selectDay)
    text(2,136,font12,255,lastDay)
    for i in range(8):
        line(0 , 17*i , 264 , 0,0)
    
    for i in range(3):
        react(22+i*86,0,65,136,255,1)

    react(194,0,68,136,255,1)
    for i in range(8):
        for x in range(3):
            if days[x+1][selectTime-4+i] ==1:
                #print(days[selectTime-4+i,x+1])
                react(x*88,i*17,88,17,0,1) 
                text(2+x*88,3+i*17,font12,255,str(selectTime-4+i)+":00")


            else:
                #print(days[selectTime-4+i,x+1])
                text(2+x*88,3+i*17,font12,0,str(selectTime-4+i)+":00")

    epd.display(epd.getbuffer(Himage))
    

    #logging.info("Clear...")
    #epd.Clear(0xFF)
    #logging.info("Goto Sleep...")
    

def handleBtnPress(btn):
    pinNum = btn.pin.number
    switcher = {
        5: "Hello, World!",
        6: "This is my first \nRPi project.",
        13: "Hope you lik it.",
    }
    if pinNum == 19:
        return on == False

    if pinNum == 13:
        selectTime += 1
        run(currentDay,selectDay,nextDay,lastDay,currentTime,selectTime,dayScroll,days)
    msg = switcher.get(pinNum, "Error")
    print(msg)


try:
    print(2)
    run(currentDay,selectDay,nextDay,lastDay,currentTime,selectTime,dayScroll,days)
    while on:
        if key1.is_pressed == True:
            selectTime -= 1
            run(currentDay,selectDay,nextDay,lastDay,currentTime,selectTime,dayScroll,days)
            print("kage1")
            time.sleep(0.5)
        if key2.is_pressed == True:
            selectTime += 1
            run(currentDay,selectDay,nextDay,lastDay,currentTime,selectTime,dayScroll,days)
            print("kage2")
            time.sleep(0.5)
        key4.when_pressed = handleBtnPress
    print(1)
    

except IOError as e:
    logging.info(e)
    
except KeyboardInterrupt:    
    logging.info("ctrl + c:")
    epd2in7.epdconfig.module_exit(cleanup=True)
    exit()





