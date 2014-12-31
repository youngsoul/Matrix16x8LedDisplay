__author__ = 'youngsoul'
import time
from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw
import math
from Adafruit_LED_Backpack import Matrix8x8

# display string that fits in number of displays
num_displays = 4

message = "Car".upper()


font = ImageFont.truetype("/usr/share/fonts/truetype/freefont/FreeMono.ttf", 10)

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


# Image.new("colors", (width,height), 'color')
im = Image.new("1", (8*num_displays, 8), "black")

empty_image = im.copy()
draw = ImageDraw.Draw(im)
width, ignore = font.getsize(message)

if width > (8*num_displays):
    print("Message does not fit in displays: " + str(width) + "," + str(8*num_displays))
    exit(-1)

print("width: " + str(width))
print("pre floor: " + str(((8*num_displays) - width) / 2))
x_offset = math.floor(((8*num_displays) - width) / 2)

# draw the text in an image rectangle the size of all of the display
# led packs.
# coordinates are those of the box.
# x1,y1,x2,y2
# x1,y1 are upper left corner
# x2,y2 are lower right corner
draw.rectangle((0, 0, 7*num_displays, 7), outline=0, fill=0)
draw.text((x_offset, 0), message, 1, font=font)

#im.save("./images/display_image.jpg", "JPEG")

# crop out the image for each of the displays
start_x = 0
height = 8
display_width = 8
end_x = start_x + display_width
# crop(x,y,w,h)
if num_displays >= 1:
    #im.crop((start_x, 0, end_x, 7)).save("./images/display1_image.jpg", "JPEG")
    print("Crop size: " + str(im.crop((start_x, 0, end_x, 8)).size))
    display1.set_image(im.crop((0, 0, 8, 8)).rotate(90))
    display1.write_display()

if num_displays >= 2:
    start_x = end_x+1
    end_x = start_x + width
#    im.crop((start_x, 0, end_x, 7)).save("./images/display2_image.jpg", "JPEG")
    print("display2 crop size: " + str(im.crop((8, 0, width-16, 8)).size))
    display2.set_image(im.crop((8, 0, 16, 8)).rotate(90))
    display2.write_display()

if num_displays >= 3:
    start_x = end_x+1
    end_x = start_x + width
#    im.crop((start_x, 0, end_x, 7)).save("./images/display3_image.jpg", "JPEG")
    display3.set_image(im.crop((16, 0, 24, height)).rotate(90))
    display3.write_display()

if num_displays >= 4:
    start_x = end_x+1
    end_x = start_x + width
#    im.crop((start_x, 0, end_x, 7)).save("./images/display4_image.jpg", "JPEG")
    display4.set_image(im.crop((24, 0, 32, height)).rotate(90))
    display4.write_display()

