Matrix16x8LedDisplay
====================

Demonstration using Python to display messages on the Adafruit 16x8 LED Backback

This project has some helper classes and python modules which can be helpful in
displaying scrolling messages, shapes and the time of day on the

Adafruit 16x8 1.2'' LED Matrix+LED Backpack.

http://www.adafruit.com/products/2042

This code was inspired heavily by the Matrix8x8.py code provided by Adafruit and the
sample trinket scrolling code.  I wanted to incorporate scrolling from the
Raspberry PI and therefore wanted a python solution so I created this git repo.

This repo does use the Adafruit libraries which I copied into my repo only to colocate
the working version with my version.  The latest versions can be found here:

https://github.com/adafruit/Adafruit_Python_LED_Backpack
https://github.com/adafruit/Adafruit_Python_GPIO

The code assumes an orientation of the LED Backpack such that the 0,0 pixel
is the upper left corner where left is the same side as the connector.

setup.sh

Simple setup script to get the raspberry pi setup to display messages.

Matrix16x8.py

This class is very similar to the Adafruit Matrix8x8 but will scroll across the
16 LEDs using a bitmap font.  You can test the Matrix16x8.py with the following
command on the Raspberry pi ( assuming you have everything configured.  See
setup.sh )

sudo python Matrix16x8.py

Matrix16x8TTF.py

This class is similar to Matrix16x8.py except that it uses TTF font and creates an
image of the text and scrolls the image.  If you want to use a TTF font that looks
good on a 16x8 matrix display, you can use this class to display messages.  It
does not perform as well while creating the images, but once created it scrolls
very smoothly.

sudo python Matrix16x8TTF.py

showtime16x8.py

This test file will show the time on the LED matrix, blinking the colon to show
it is working every second.

tools/16x8Matrix-Numbers09.numbers

This is a spreadsheet I used to create some of the bitmap letters, numbers and
shapes.  If you type a 1 into a cell, it will change the color and give you
the hex value for the column.

Youtube demo:

https://www.youtube.com/watch?v=PTNiumuMFHg&list=UUMMOWGymcHR5Wde_c1Z0P0w

