import sys
import os
path = "//home/pi/Documents/ungdom/Test/pic"

import logging
from waveshare_epd import epd2in7
import time
from PIL import Image,ImageDraw,ImageFont
import traceback


def line(x,y,xp,yp,fill):
    return draw.line((x, y, xp, yp), fill = fill)