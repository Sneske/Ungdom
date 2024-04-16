from waveshare_epd import epd2in7b
import time
from PIL import Image,ImageDraw,ImageFont

try:
    epd = epd2in7b.EPD()
    epd.init()
    epd.Clear()

    font24 = ImageFont.truetype('pic/Font.ttc', 24)

    HBlackimage = Image.new('1', (epd.height, epd.width), 255)  # 298*126
    HRedimage = Image.new('1', (epd.height, epd.width), 255)  # 298*126

    drawblack = ImageDraw.Draw(HBlackimage)
    drawred = ImageDraw.Draw(HRedimage)

    drawblack.text((10, 0), 'Hej Verden!', font = font24, fill = 0)
    drawred.text((10, 40), 'Vi tester e-Paper', font=font24, fill=0)
    epd.display(epd.getbuffer(HBlackimage), epd.getbuffer(HRedimage))
    time.sleep(5)
    drawblack.text((10,80), 'Det er sjovt', font=font24, fill=0)
    epd.display(epd.getbuffer(HBlackimage), epd.getbuffer(HRedimage))
    time.sleep(5)

    epd.init()
    epd.Clear()
    epd.sleep()

except IOError as e:
    print(e)