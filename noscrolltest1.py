__author__ = 'youngsoul'

import time

import MultiMatrix8x8Display


time1 = time.strftime("%I:%M")
if time1.startswith("0"):
    time1 = time1[1:]
time2 = time1+"."


d = MultiMatrix8x8Display(repeat_delay=0, scroll_delay=0.05, font_size=10, font_path="/home/pi/dev/MatrixDisplay/fonts/SFPixelate.ttf")
x = d.get_starting_x_position(time2)
while True:
    d.display_message(time1,x_position=x)
    time.sleep(1)
    d.display_message(time2,x_position=x)
    time.sleep(1)
    d.display_message(time1,x_position=x)
    time.sleep(1)
    d.display_message(time2,x_position=x)
    time.sleep(1)
    d.display_message(time1,x_position=x)
    time.sleep(1)
    d.display_message(time2,x_position=x)
    time.sleep(1)
    d.display_message(time1,x_position=x)
    time.sleep(1)
    d.display_message(time2,x_position=x)
    time.sleep(1)
    d.scroll_message("Show on multiple 8x8 matrix displays", y_position=1)
    time.sleep(1)
