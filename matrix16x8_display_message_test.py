__author__ = 'youngsoul'

import time

import Matrix16x8TTF


matrix = Matrix16x8TTF(font_path="/home/pi/dev/MatrixDisplay/fonts/PressStart2P.ttf", brightness=1,repeat_delay=0, scroll_delay=0.02, rotate_text=False, font_size=8)

hour = time.strftime("%I")
minute = time.strftime("%M")
am_pm = time.strftime("%p")
if hour.startswith("0"):
    hour = hour[1:]
matrix.display_message(message=hour)
time.sleep(2)
matrix.display_message(message=minute)
time.sleep(2)
matrix.display_message(message=am_pm)
time.sleep(2)

matrix.clear()