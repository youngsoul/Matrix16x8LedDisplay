__author__ = 'youngsoul'

# 70 - display 1
# 72 - display 2
# 71 - display 3
# 74 - display 4
import math
import time
import platform

from Matrix16x8 import Matrix16x8


if platform.system() == "Linux":
    from PIL import ImageFont
    from PIL import Image
    from PIL import ImageDraw


class Matrix16x8Display(object):

    def __init__(self, display1_address=0x70, repeat_delay=0, scroll_delay=0.05, brightness=4, rotate_text=True, font_size=9, font_path="/home/pi/dev/MatrixDisplay/fonts/SFPixelate.ttf"):
        self.rotate_text = rotate_text
        self.brightness = brightness
        self.repeat_delay = repeat_delay
        self.scroll_delay = scroll_delay
        self.font_path = font_path
        self.font_size = font_size
        self.standard_width = 16
        self.standard_height = 8

        if display1_address:
            self.display1 = Matrix16x8(address=display1_address)
            self.display1.set_brightness(self.brightness)
            self.display1.begin()
        else:
            self.display1 = None

#        self.font = ImageFont.truetype("/usr/share/fonts/truetype/freefont/FreeSansBold.ttf", 9)
        self.font = ImageFont.truetype(self.font_path, self.font_size)

        self.empty_image = None
        self.images = None
        self.images_message = None
        self.delay_time = 0.1

    def set_font(self, imageFont):
        self.font = imageFont

    def set_delay_time(self, delay_time):
        self.delay_time = delay_time

    def clear(self):
        if self.empty_image is not None:
            if self.display1:
                self.display1.set_image(self.empty_image)
                self.display1.write_display()

        self.images = None

    def scroll_message(self, display_message="", num_scrolls=1):

        # width of double led pack
        x_width = self.standard_width

        # create new Image class for single color, 8x8 LED Pack with a black background
        im = Image.new("1", (self.standard_width, self.standard_height), "black")

        # copy the empty image so it can be used to fill empty frames
        if self.empty_image is None:
            self.empty_image = im.copy()

        draw = ImageDraw.Draw(im)
        display_message = display_message.upper()
        width, ignore = self.font.getsize(display_message)

        x_index = 16  # start right at the far right edge.

        # create the images that would scroll through a single led pack
        # save the images in an image array, so that each of the led packs
        # can display the data when necessary
        y_offset = 0

        if self.images_message != display_message:
            # then any previous images data is invalid:
            self.images = None
            self.images_message = display_message

        image_index = 0
        if self.images is None:
            self.images = []
            while x_index >= -width:
                x_index = x_index - 1
                draw.rectangle((0, 0, 15, 7), outline=0, fill=0)
                draw.text((x_index, 0), display_message, 1, font=self.font)
                y_offset += 1
                # save the image at this particular x value
                if self.rotate_text:
                    the_im = im.copy().rotate(90)
#                    the_im.save("./images/image_"+str(image_index)+".jpg", "JPEG")
                    self.images.append(the_im)
                    image_index += 1
                else:
                    the_im = im.copy()
#                    the_im.save("./images/image_"+str(image_index)+".jpg", "JPEG")
                    self.images.append(im.copy())
                    image_index += 1

        self.display1.set_brightness(self.brightness)

        while num_scrolls > 0 or num_scrolls <= -1:
            num_scrolls -= 1

            # displays are numbered from left to right
            # display_1 is the far left display
            # these indexes are negatively displaced such that
            # display1 is the most negatively displaced to the left so it is the
            # last display to get the data.
            display1_index = -x_width

            # loop through all of the displays and shift in the
            while display1_index < len(self.images):
                if display1_index >= -1 and display1_index < len(self.images):
                    self.display1.set_image(self.images[display1_index])
                    self.display1.write_display()
                else:
                    self.display1.set_image(self.empty_image)
                    self.display1.write_display()

                display1_index += 1
                time.sleep(self.scroll_delay) #this time governs the speed of the scroll

            # if the param is passed in, consider it an override for the class level
            # this section governs the time between scrolling messages
            time.sleep(self.repeat_delay)

    def display_message(self, message, align='Center', x_position=None):
        # create new Image class for single color, 8x8 LED Pack with a black background
        im = Image.new("1", (self.standard_width, self.standard_height), "black")

        # copy the empty image so it can be used to fill empty frames
        if self.empty_image is None:
            self.empty_image = im.copy()

        draw = ImageDraw.Draw(im)
        display_message = message.upper()
        width, ignore = self.font.getsize(display_message)

        # if width > 16:
        #     print("Message does not fit")
        #     return

        x_offset = 1
        if x_position is None:
            if align is 'Left':
                x_offset = 1
            elif align is 'Center':
                x_offset = max(1, math.floor((self.standard_width - width) / 2))
        else:
            x_offset = x_position

        # draw the text in an image rectangle the size of all of the display
        # led packs.
        # coordinates are those of the box.
        # x1,y1,x2,y2
        # x1,y1 are upper left corner
        # x2,y2 are lower right corner
        draw.rectangle((0, 0, self.standard_width, self.standard_height), outline=0, fill=0)
        draw.text((x_offset, 1), message, 1, font=self.font)
        self.display1.set_image(im)
        self.display1.set_brightness(self.brightness)
        self.display1.write_display()



if __name__ == '__main__':

    matrix = Matrix16x8Display(brightness=0, rotate_text=False, repeat_delay=0, scroll_delay=0.02)

    matrix = Matrix16x8Display(font_path="/home/pi/dev/MatrixDisplay/fonts/PressStart2P.ttf", brightness=4, repeat_delay=0, scroll_delay=0.02, rotate_text=False)
    matrix.scroll_message(display_message="The quick brown fox jumps over the lazy dog.  PressStart2P.ttf", num_scrolls=1)
    matrix = Matrix16x8Display(font_path="/home/pi/dev/MatrixDisplay/fonts/8BitWonder.ttf", brightness=4, repeat_delay=0,scroll_delay=0.02, rotate_text=False)
    matrix.scroll_message(display_message="The quick brown fox jumps over the lazy dog.  8BitWonder.ttf", num_scrolls=1)
    matrix = Matrix16x8Display(font_path="/home/pi/dev/MatrixDisplay/fonts/SFPixelate.ttf", brightness=4, repeat_delay=0,scroll_delay=0.02, rotate_text=False)
    matrix.scroll_message(display_message="The quick brown fox jumps over the lazy dog.  SFPixelate.ttf", num_scrolls=1)
    matrix = Matrix16x8Display(font_path="/home/pi/dev/MatrixDisplay/fonts/Starmap.ttf", brightness=4, repeat_delay=0,scroll_delay=0.02, rotate_text=False)
    matrix.scroll_message(display_message="The quick brown fox jumps over the lazy dog.  Starmap.ttf", num_scrolls=1)

    # #matrix.scroll_message("The quick brown fox jumps over the lazy dog", -1, 0)
    # messages = []
    # messages.append("Weather Conditions for Cork, IE at 3:00 am IST. Currently")
    # messages.append("Partly Cloudy, 10 degrees celcius.  ")
    # messages.append("five day Forecast.  ")
    # messages.append(".Tuesday.  Clear. High of 18 Low of 9")
    # messages.append(".Wednesday.  Partly Cloudy. High of 21 Low of 12")
    # messages.append(".Thursday.  Partly Cloudy. High of 19 Low of 12")
    # messages.append(".Friday.  Mostly Cloudy. High of 19 Low of 13")
    # messages.append(".Saturday  Partly Cloudy. High of 19 Low of 12")
    # messages.append("Full Forecast at Yahoo! Weather")
    # messages.append("provided by The Weather Channel")
    #
    # for message in messages:
    #     matrix.scroll_message(display_message=message, num_scrolls=1)
