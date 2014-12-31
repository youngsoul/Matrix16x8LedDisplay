__author__ = 'youngsoul'
# sudo pip install pil --allow-external pil

from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw

test_string = "Welcome back my friends"

font = ImageFont.truetype("/usr/share/fonts/truetype/freefont/FreeSansBold.ttf", 9)

im = Image.new("1", (8, 8), "black")
draw = ImageDraw.Draw(im)
width, ignore = font.getsize(test_string)

print("String width: " + str(width))
