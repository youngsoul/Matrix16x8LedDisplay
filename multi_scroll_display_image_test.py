__author__ = 'youngsoul'
from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw
from Adafruit_LED_Backpack import Matrix8x8

import time

message = "The quick brown fox jumps over the lazy dog".upper()

# 70 - display 1
# 72 - display 2
# 71 - display 3
# 74 - display 4

display1 = Matrix8x8.Matrix8x8(address=0x70)
display1.begin()
display2 = Matrix8x8.Matrix8x8(address=0x72)
display2.begin()
display3 = Matrix8x8.Matrix8x8(address=0x71)
display3.begin()
display4 = Matrix8x8.Matrix8x8(address=0x74)
display4.begin()

font = ImageFont.truetype("/usr/share/fonts/truetype/freefont/FreeSans.ttf", 8)
#font = ImageFont.truetype("/usr/share/fonts/truetype/freefont/FreeSansBold.ttf", 9)
# create new Image class for single color, 8x8 LED Pack with a black background
im = Image.new("1", (8, 8), "black")

# copy the empty image so it can be used to fill empty frames
empty_image = im.copy()

draw = ImageDraw.Draw(im)
width, ignore = font.getsize(message)


num_displays = 4
use_display1 = True
use_display2 = True
use_display3 = True
use_display4 = True


# collection of images that represent the frames in a single 8x8 LED Pack
images = []

# width of a single led pack
x_width = 8

# displays are numbered from left to right
# display_1 is the far left display
# these indexes are negatively displaced such that
# display1 is the most negatively displaced to the left so it is the
# last display to get the data.
display1_index = -(x_width * (num_displays-1))
display2_index = -(x_width * (num_displays-2))
display3_index = -(x_width * (num_displays-3))
display4_index = -(x_width * (num_displays-4))

x_index = 8  # start right at the far right edge.

# create the images that would scroll through a single led pack
# save the images in an image array, so that each of the led packs
# can display the data when necessary
y_offset = 0
while x_index >= -width:
    x_index = x_index - 1
    draw.rectangle((0, 0, 7, 7), outline=0, fill=0)
    draw.text((x_index, 0), message, 1, font=font)
    y_offset += 1
    # save the image at this particular x value
    images.append(im.copy().rotate(90))

# loop through all of the displays and shift in the
while display1_index < len(images):
    if use_display1:
        if display1_index >= -1 and display1_index < len(images):
            display1.set_image(images[display1_index])
            display1.write_display()
        else:
            display1.set_image(empty_image)
            display1.write_display()

    if use_display2:
        if display2_index >= -1 and display2_index < len(images):
            display2.set_image(images[display2_index])
            display2.write_display()
        else:
            display2.set_image(empty_image)
            display2.write_display()

    if use_display3:
        if display3_index >= -1 and display3_index < len(images):
            display3.set_image(images[display3_index])
            display3.write_display()
        else:
            display3.set_image(empty_image)
            display3.write_display()

    if use_display4:
        if display4_index >= -1 and display4_index < len(images):
            display4.set_image(images[display4_index])
            display4.write_display()
        else:
            display4.set_image(empty_image)
            display4.write_display()

    display1_index += 1
    display2_index += 1
    display3_index += 1
    display4_index += 1
    #time.sleep(1)