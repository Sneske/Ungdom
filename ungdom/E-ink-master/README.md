# e-Paper  
#### Slå SPI til på Raspberry Pi:

```cmd
sudo raspi-config
Choose Interfacing Options -> SPI -> Yes  to enable SPI interface
```

#### Install BCM2835 libraries:

```cmd
wget http://www.airspayce.com/mikem/bcm2835/bcm2835-1.60.tar.gz
tar zxvf bcm2835-1.60.tar.gz 
cd bcm2835-1.60/
sudo ./configure
sudo make
sudo make check
sudo make install
#For more details, please refer to http://www.airspayce.com/mikem/bcm2835/
```

#### Install wiringPi libraries:

```cmd
sudo apt-get install wiringpi

#For Pi 4, you need to update it：
cd /tmp
wget https://project-downloads.drogon.net/wiringpi-latest.deb
sudo dpkg -i wiringpi-latest.deb
gpio -v
#You will get 2.52 information if you install it correctly
```

#### Install Python libraries:

```cmd
sudo apt-get update
sudo apt-get install python3-pip
sudo apt-get install python3-pil
sudo apt-get install python3-numpy
sudo pip3 install RPi.GPIO
sudo pip3 install spidev
```

#### Clone repositoriet på Rpi'en:

`git clone https://github.com/unord/E-ink.git`

#### Kør setup.py:

`sudo python3 setup.py install`

#### Test at det virker:

`python3 epd_2in7b_test.py`

#### Links:

https://healeycodes.com/hacking-together-an-e-ink-dashboard/

https://www.waveshare.com/wiki/2.7inch_e-Paper_HAT_(B)

https://github.com/waveshare/e-Paper

https://pypi.org/project/epd-library/

Her er et sjovt projekt med e-Paper Hat'en:

https://github.com/protostax/ProtoStax_ISS_Tracker



