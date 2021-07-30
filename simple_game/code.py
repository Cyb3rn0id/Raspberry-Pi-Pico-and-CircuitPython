# simple game with 8x8 ws2812 matrix and analog joystick
# board used is a Cytron Maker Pi Pico
# language is CircuitPython
# by @cyb3rn0id
# https://www.settorezero.com
# needed libraries:
# lcd by Dan Halbert: https://github.com/dhalbert/CircuitPython_LCD
# adafruit_bus_device
# neopixel

import time
import board
import neopixel
import busio
import random
import pwmio
from analogio import AnalogIn
from lcd.lcd import LCD
from lcd.i2c_pcf8574_interface import I2CPCF8574Interface

tones = {
    '0':    1,
    'B0':  31,
    'C1':  33,
    'CS1': 35,
    'D1':  37,
    'DS1': 39,
    'E1':  41,
    'F1':  44,
    'FS1': 46,
    'G1':  49,
    'GS1': 52,
    'A1':  55,
    'AS1': 58,
    'B1':  62,
    'C2':  65,
    'CS2': 69,
    'D2':  73,
    'DS2': 78,
    'E2':  82,
    'F2':  87,
    'FS2': 93,
    'G2':  98,
    'GS2': 104,
    'A2':  110,
    'AS2': 117,
    'B2':  123,
    'C3':  131,
    'CS3': 139,
    'D3':  147,
    'DS3': 156,
    'E3':  165,
    'F3':  175,
    'FS3': 185,
    'G3':  196,
    'GS3': 208,
    'A3':  220,
    'AS3': 233,
    'B3':  247,
    'C4':  262,
    'CS4': 277,
    'D4':  294,
    'DS4': 311,
    'E4':  330,
    'F4':  349,
    'FS4': 370,
    'G4':  392,
    'GS4': 415,
    'A4':  440,
    'AS4': 466,
    'B4':  494,
    'C5':  523,
    'CS5': 554,
    'D5':  587,
    'DS5': 622,
    'E5':  659,
    'F5':  698,
    'FS5': 740,
    'G5':  784,
    'GS5': 831,
    'A5':  880,
    'AS5': 932,
    'B5':  988,
    'C6':  1047,
    'CS6': 1109,
    'D6':  1175,
    'DS6': 1245,
    'E6':  1319,
    'F6':  1397,
    'FS6': 1480,
    'G6':  1568,
    'GS6': 1661,
    'A6':  1760,
    'AS6': 1865,
    'B6':  1976,
    'C7':  2093,
    'CS7': 2217,
    'D7':  2349,
    'DS7': 2489,
    'E7':  2637,
    'F7':  2794,
    'FS7': 2960,
    'G7':  3136,
    'GS7': 3322,
    'A7':  3520,
    'AS7': 3729,
    'B7':  3951,
    'C8':  4186,
    'CS8': 4435,
    'D8':  4699,
    'DS8': 4978,
}

# setup
pixel_pin = board.GP0
matrix_width = 8
matrix_height = 8

# I2C interface on Grove 4 connector of Maker Pi Pico
i2c = busio.I2C(board.GP7, board.GP6)  # SCL (yellow), SDA (white)

# Talk to the LCD at I2C address 0x27 (default on PCF8574 backpacks)
# using the i2c interface previously created
# The number of rows and columns defaults to 4x20, so those
# arguments could be omitted in this case.
lcd = LCD(I2CPCF8574Interface(i2c, 0x27), num_rows=4, num_cols=20)
lcd.clear()

# matrix init
pixels = neopixel.NeoPixel(
    pixel_pin, (matrix_width * matrix_height), brightness=0.2, auto_write=True
)

# analog pins
joy_x = AnalogIn(board.A1)  # GP27
joy_y = AnalogIn(board.A0)  # GP26

# Initialize buzzer
buzzer = pwmio.PWMOut(board.GP18, variable_frequency=True)

# seed pixel
seedPix = 0

# score
score = 0

# melodies
up = ['E4', 'D4', 'C4']

# some default colors (R, G, B)
RED = (255, 0, 0)
YELLOW = (255, 150, 0)
GREEN = (0, 255, 0)
CYAN = (0, 255, 255)
BLUE = (0, 0, 255)
PURPLE = (180, 0, 255)
BLACK = (0, 0, 0)  # pixel off

def music():
    for i in up:
        buzzer.frequency = tones[i]
        buzzer.duty_cycle = 19660
        time.sleep(0.15)
    buzzer.duty_cycle = 0

def pixel2coord(pix):
    y = pix // 8
    x = pix % 8
    return (x, y)

def coord2pixel(x, y):
    pix = (matrix_width * y) + x
    return pix


# Y su=65000, giu=0
# X dx=zero, sx=65000
# deadzone=30-40k

# start random number generator
random.seed(joy_x.value)

# create new random pixel
def randSeed():
    return (random.randint(0, (matrix_height * matrix_width) - 1))

# place the new random pixel
def placeSeed():
    p = randSeed()
    while (p == myPix):
        p = randSeed()
    global seedPix
    seedPix = p
    pixels[seedPix] = RED

newSeed = True
# pixel start position
myPix = (matrix_height * matrix_width) // 2
myPixCoord = pixel2coord(myPix)
# set start pixel
pixels[myPix] = GREEN

lcd.set_cursor_pos(0, 0)
lcd.print("** 7000 FOLLOWERS **")
lcd.set_cursor_pos(1, 0)
lcd.print("*FOLLOW  @cyb3rn0id*")

while True:
    ax = joy_x.value
    ay = joy_y.value

    # set_cursor_pos(line, column) - 0-based index
    lcd.set_cursor_pos(2, 0)
    lcd.print("SCORE: ")
    lcd.print(str(score))
    lcd.set_cursor_pos(3, 0)
    lcd.print("x: ")
    lcd.print(str(ax))
    lcd.print(" y: ")
    lcd.print(str(ay))
    lcd.print(" ")

    # place the new seed if needed
    if (newSeed):
        newSeed = False
        placeSeed()

    # previous pixel position
    x = myPixCoord[0]
    y = myPixCoord[1]
    dx = x
    dy = y

    # check joystick x value
    if ax > 40000:
        # move left
        x = x - 1
        if x < 0:
            x = 0
    elif ax < 30000:
        # move right
        x = x + 1
        if x == matrix_width:
            x = matrix_width - 1

    # check joystick y value
    if ay > 40000:
        # move up
        y = y - 1
        if y < 0:
            y = 0
    elif ay < 30000:
        # move down
        y = y + 1
        if y == matrix_height:
            y = matrix_height - 1

    # pixel has moved
    if (x != dx) or (y != dy):

        # set new pixel
        myPix = coord2pixel(x, y)
        myPixCoord = (x, y)

        # player hit the seed
        if (myPix == seedPix):
            # delete quick the previous pixel
            pixels[coord2pixel(dx, dy)] = BLACK
            # change color to actual pixel
            pixels[myPix] = (255, 255 , 0)
            score = score + 1
            newSeed = True
            music()

        pixels[myPix] = GREEN
        # delete previous pixel
        pixels[coord2pixel(dx, dy)] = BLACK
