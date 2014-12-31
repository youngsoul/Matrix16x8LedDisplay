__author__ = 'youngsoul'

from Matrix16x8 import Matrix16x8
import time
from fonts import custom_font

m = Matrix16x8()

hours_colon = custom_font.hours
hours_no_colon = custom_font.hours_no_colon
digits = custom_font.digits


colon_on = True

while True:
    the_hour = time.strftime("%I")
    the_min = time.strftime("%M")
    if the_hour.startswith("0"):
        the_hour = the_hour[1:]

    if colon_on:
        colon_on = False
        the_hour_data = hours_colon[the_hour]
    else:
        colon_on = True
        the_hour_data = hours_no_colon[the_hour]

    the_min_data =  digits[the_min[0]]+digits[the_min[1]]
    buffer = the_hour_data + the_min_data
    m.display_16x8_buffer(buffer)

    time.sleep(1)



