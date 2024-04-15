import wx
import gui
from PIL import Image,ImageDraw,ImageFont
import threading
from waveshare_epd import epd2in7b

class mainFrame(gui.MainFrame):
    def __init__(self, parent):
        gui.MainFrame.__init__(self, parent)
        self.epd = epd2in7b.EPD()
        self.epd.init()
        self.epd.Clear()
        self.font24 = ImageFont.truetype('pic/Font.ttc', 24)

    def skriv_ud(self, antal, tekst):
        self.HBlackimage = Image.new('1', (self.epd.height, self.epd.width), 255)  # 298*126
        self.HRedimage = Image.new('1', (self.epd.height, self.epd.width), 255)  # 298*126
        self.drawblack = ImageDraw.Draw(self.HBlackimage)
        self.drawred = ImageDraw.Draw(self.HRedimage)
        if self.m_radioBox1.GetSelection() == 0:
            self.drawblack.text((10, 0), tekst, font=self.font24, fill=0)
        else:
            self.drawred.text((10,0), tekst, font=self.font24, fill=0)
        self.epd.display(self.epd.getbuffer(self.HBlackimage), self.epd.getbuffer(self.HRedimage))
        self.m_button1.Enable()

    def afslut(self, event):
        self.epd.init()
        self.epd.Clear()
        self.epd.sleep()
        exit(0)

    def send_to_eink( self, event ):
        self.tekst = self.eink_txt.GetValue()
        thread = threading.Thread(target=self.skriv_ud, args = (1,self.tekst))
        thread.start()
        self.m_button1.Disable()

app = wx.App(False)
frame = mainFrame(None)
frame.Show(True)
app.MainLoop()