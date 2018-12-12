#!usr/bin/python
from time import sleep
import RPi.GPIO as GPIO
import urllib.request

# Import the WS2801 module.
import Adafruit_WS2801
import Adafruit_GPIO.SPI as SPI


# Configure the count of pixels:
PIXEL_COUNT = 96

# Specify a hardware SPI connection on /dev/spidev0.0:
SPI_PORT   = 0
SPI_DEVICE = 0
pixels = Adafruit_WS2801.WS2801Pixels(PIXEL_COUNT, spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE), gpio=GPIO)

from flask import (
    Flask,
    render_template,
    request,
)

app = Flask(__name__)

@app.route('/lights/levelColor', methods=['GET', 'POST'])

#/levelColor?color=orange&level=50
# Set Colour Level

def setLevelColor():
    pixels.clear()

    color = urllib.request.unquote(request.values['color']).strip()
    number = int(urllib.request.unquote(request.values['level']).strip())

    if color.lower().__contains__("orange"):
        pixels.clear()
        for k in range(pixels.count()):
            pixels.set_pixel(k, Adafruit_WS2801.RGB_to_color(255,127,80))
        pixels.show()
    elif color.lower().__contains__("white"):
        pixels.clear()
        for k in range(pixels.count()):
            pixels.set_pixel(k, Adafruit_WS2801.RGB_to_color(255,255,255))
        pixels.show()
    else:
        for k in range(pixels.count()):
            pixels.set_pixel(k, Adafruit_WS2801.RGB_to_color(255,234,76))
        pixels.show()

    return "Color: %s Level: %s\n" % (color, number)


@app.route('/lights/party', methods=['GET', 'POST'])

#/levelColor
# Set Colour Level

def setLevelColor():
    pixels.clear()

    for i in range(pixels.count()):
    # tricky math! we use each pixel as a fraction of the full 96-color wheel
    # (thats the i / strip.numPixels() part)
    # Then add in j which makes the colors go around per pixel
    # the % 96 is to make the wheel cycle around
    pixels.set_pixel(i, wheel(((i * 256 // pixels.count())) % 256) )
    pixels.show()
    time.sleep(0.5)

    return "PARTY!!\n"

@app.route('/lights/power', methods=['GET', 'POST'])

def power():

    state = urllib.request.unquote(request.values['state']).strip().lower()
    if state.__contains__("off"):
        pixels.clear()
        pixels.show()
    elif state.__contains__("on"):
        pixels.clear()
        for k in range(pixels.count()):
            pixels.set_pixel(k, Adafruit_WS2801.RGB_to_color(255,228,206))
        pixels.show()

    return "Lights set to %s\n" % (state)

if __name__ == "__main__":
    app.run('0.0.0.0', 5300, debug=True)
