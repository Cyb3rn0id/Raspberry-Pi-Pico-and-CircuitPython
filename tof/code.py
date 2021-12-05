# Test display HD44780 with PCF8574 Backpack by @cyb3rn0id
# Library by Dan Halbert:
# https://github.com/dhalbert/CircuitPython_LCD

import board
import busio
import time
from lcd.lcd import LCD
from lcd.i2c_pcf8574_interface import I2CPCF8574Interface

import adafruit_vl53l0x

# I2C interface on Grove 4 connector
# of Maker Pi Pico
i2c = busio.I2C(board.GP7, board.GP6)  # SCL (yellow), SDA (white)

# Talk to the LCD at I2C address 0x27 (default on PCF8574 backpacks)
# using the i2c interface previously created
# The number of rows and columns defaults to 4x20, so those
# arguments could be omitted in this case.
lcd = LCD(I2CPCF8574Interface(i2c, 0x27), num_rows=4, num_cols=20)

# Initialize second I2C bus for laser sensor
# sda, scl
i2c2 = busio.I2C(board.GP5, board.GP4)
vl53 = adafruit_vl53l0x.VL53L0X(i2c2)

# set_cursor_pos(line, column) - 0-based index
lcd.clear()
lcd.set_cursor_pos(0, 0)
lcd.print("VL53L0X Test")
lcd.set_cursor_pos(1, 0)
lcd.print("Maker Pi Pico")
lcd.set_cursor_pos(2, 0)
lcd.print("Distance: ")
lcd.set_cursor_pos(3, 0)
lcd.print("FOLLOW @CyB3rn0id")
time.sleep(2)

while True:
    r = (vl53.range / 10) - 3
    # r = 10
    lcd.set_cursor_pos(2, 10)
    lcd.print(str(r))
    lcd.print("cm  ")
    time.sleep(0.2)
