### Simple game for Raspberry Pi Pico

This is a quick game I made for the 7k followers on IG: [video](https://www.instagram.com/reel/CR9dZVVj7tu/)

#### Board
Raspberry Pi Pico attached on the [Cytron Maker Pi Pico](https://www.settorezero.com/wordpress/sperimentare-con-raspberry-pi-pico-maker-pi-rp2040-pico/)

#### Devices attached
- LCD display 20x4 having PCF8574 I2C Backpack - connected to GROVE 4 (yellow=SCL=GP7, white=SDS=GP6) ([tips'n tricks](https://www.settorezero.com/wordpress/utilizzare-un-display-lcd-a-caratteri-con-circuitpython/))
- 8x8 RGB Matrix (WS2812) - Data on GP0
- Analog Thumbstick on GROVE 6 (yellow=X_axis=GP27=ADC1, white=Y_axis=GP26=ADC0)

Used the Maker Pi Pico Buzzer (GP18)

#### Libraries to be installed
- [lcd by Dan Halbert](https://github.com/dhalbert/CircuitPython_LCD) (copy entire folder)
- from [adafruit bundle](https://circuitpython.org/libraries): adafruit_bus_device (copy entire folder)
- from [adafruit bundle](https://circuitpython.org/libraries): neopixel (neopixel.mpy)