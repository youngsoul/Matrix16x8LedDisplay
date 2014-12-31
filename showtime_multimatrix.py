__author__ = 'youngsoul'

import time

import MultiMatrix8x8Display


time1 = time.strftime("%I:%M")
if time1.startswith("0"):
    time1 = time1[1:]
time2 = time1+"."
new_time1 = time1
new_time2 = time2

d = MultiMatrix8x8Display(repeat_delay=0, scroll_delay=0.05, font_size=10, font_path="/home/pi/dev/MatrixDisplay/fonts/SFPixelate.ttf")
x = d.get_starting_x_position(time2)
while True:

    new_time1 = time.strftime("%I:%M")
    if new_time1.startswith("0"):
        new_time1 = new_time1[1:]
    if new_time1 != time1:
        time1 = new_time1
        new_time2 = new_time1+"."

    x = d.get_starting_x_position(new_time2)
    d.display_message(new_time1,x_position=x)
    time.sleep(1)
    d.display_message(new_time2,x_position=x)
    time.sleep(1)

