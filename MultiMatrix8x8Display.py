__author__ = 'youngsoul'

# 70 - display 1
# 72 - display 2
# 71 - display 3
# 74 - display 4
from Adafruit_LED_Backpack import Matrix8x8
import time
import platform
import math
import hashlib
import base64
import os.path

if platform.system() == "Linux":
    from PIL import ImageFont
    from PIL import Image
    from PIL import ImageDraw


class MultiMatrix8x8Display(object):

    def __init__(self, message_cache_dir=None, repeat_delay=0, scroll_delay=0, display1_address=0x70, display2_address=0x72, display3_address=0x71, display4_address=0x74, font_size=9, font_path="/usr/share/fonts/truetype/freefont/FreeSansBold.ttf"):
        self.num_displays = 0
        self.use_display1 = False
        self.use_display2 = False
        self.use_display3 = False
        self.use_display4 = False
        self.rotate_text = True
        self.repeat_delay = repeat_delay
        self.scroll_delay = scroll_delay
        self.message_cache_dir = message_cache_dir

        if display1_address:
            self.display1 = Matrix8x8.Matrix8x8(address=display1_address)
            self.display1.begin()
            self.num_displays += 1
            self.use_display1 = True
        else:
            self.display1 = None

        if display2_address:
            self.display2 = Matrix8x8.Matrix8x8(address=display2_address)
            self.display2.begin()
            self.num_displays += 1
            self.use_display2 = True
        else:
            self.display2 = None

        if display3_address:
            self.display3 = Matrix8x8.Matrix8x8(address=display3_address)
            self.display3.begin()
            self.num_displays += 1
            self.use_display3 = True
        else:
            self.display3 = None

        if display4_address:
            self.display4 = Matrix8x8.Matrix8x8(address=display4_address)
            self.display4.begin()
            self.num_displays += 1
            self.use_display4 = True
        else:
            self.display4 = None

        self.font = ImageFont.truetype(font_path, font_size)

        self.empty_image = None
        self.images = None
        self.images_message = None
        self.delay_time = 0.1

    def set_font(self,imageFont):
        self.font = imageFont

    def set_delay_time(self,delay_time):
        self.delay_time = delay_time

    def clear(self):
        if self.empty_image is not None:
            if self.display1:
                self.display1.set_image(self.empty_image)
                self.display1.write_display()

            if self.display2:
                self.display2.set_image(self.empty_image)
                self.display2.write_display()

            if self.display3:
                self.display3.set_image(self.empty_image)
                self.display3.write_display()

            if self.display4:
                self.display4.set_image(self.empty_image)
                self.display4.write_display()

        self.images = None

    @staticmethod
    def _create_base64_md5_hash(string_to_hash):
        if isinstance(string_to_hash, unicode):
            string_to_hash_as_bytes = unicode.encode(string_to_hash)
        else:
            string_to_hash_as_bytes = str.encode(string_to_hash)

        md5_hash_string = hashlib.md5(string_to_hash_as_bytes).hexdigest()
        md5_as_base64_bytes = base64.standard_b64encode(str.encode(md5_hash_string))
        md5_as_base64_string = md5_as_base64_bytes.decode('ascii')
        return md5_as_base64_string

    def scroll_message(self, message, num_scrolls=1, y_position=0):

        message_hash = MultiMatrix8x8Display._create_base64_md5_hash(message)
        #print("message_hash: " + message_hash)

        # width of a single led pack
        x_width = 8

        # create new Image class for single color, 8x8 LED Pack with a black background
        im = Image.new("1", (8, 8), "black")

        # copy the empty image so it can be used to fill empty frames
        if self.empty_image is None:
            self.empty_image = im.copy()

        draw = ImageDraw.Draw(im)
        message = message.upper()
        width, ignore = draw.textsize(message, font=self.font)

        x_index = 8  # start right at the far right edge.

        # create the images that would scroll through a single led pack
        # save the images in an image array, so that each of the led packs
        # can display the data when necessary
        y_offset = y_position

        if self.images_message != message:
            # then any previous images data is invalid:
            self.images = None
            self.images_message = message

        if self.images is None and self.message_cache_dir is not None:
            # then we do not have the message already in the memory buffer
            # check to see if we have the image files generated:
            if os.path.isfile(self.message_cache_dir+"/"+message_hash+"_"+str(0)+".jpg"):
                # then we have already created the files so just read them.
                self.images = []
                image_index = 0
                while os.path.isfile(self.message_cache_dir+"/"+message_hash+"_"+str(image_index)+".jpg"):
                    tmp_image = Image.open(self.message_cache_dir+"/"+message_hash+"_"+str(image_index)+".jpg")
                    tmp_image.load()
                    self.images.append(tmp_image)
                    image_index += 1

        if self.images is None:
            self.images = []
            while x_index >= -width:
                x_index = x_index - 1
                draw.rectangle((0, 0, 7, 7), outline=0, fill=0)
                draw.text((x_index, y_offset), message, 1, font=self.font)
                # save the image at this particular x value
                if self.rotate_text:
                    self.images.append(im.copy().rotate(90))
                else:
                    self.images.append(im.copy())

            if self.message_cache_dir is not None and len(self.images) > 200:
                #then we should cache these message images
                image_index = 0
                for image in self.images:
                    image.save(self.message_cache_dir+"/"+message_hash+"_"+str(image_index)+".jpg", "JPEG")
                    image_index += 1

        while num_scrolls > 0 or num_scrolls <= -1:
            num_scrolls -= 1

            # displays are numbered from left to right
            # display_1 is the far left display
            # these indexes are negatively displaced such that
            # display1 is the most negatively displaced to the left so it is the
            # last display to get the data.
            display1_index = -(x_width * (self.num_displays-1))
            display2_index = -(x_width * (self.num_displays-2))
            display3_index = -(x_width * (self.num_displays-3))
            display4_index = -(x_width * (self.num_displays-4))

            # loop through all of the displays and shift in the
            while display1_index < len(self.images):
                if self.use_display1:
                    if display1_index >= -1 and display1_index < len(self.images):
                        self.display1.set_image(self.images[display1_index])
                        self.display1.write_display()
                    else:
                        self.display1.set_image(self.empty_image)
                        self.display1.write_display()

                if self.use_display2:
                    if display2_index >= -1 and display2_index < len(self.images):
                        self.display2.set_image(self.images[display2_index])
                        self.display2.write_display()
                    else:
                        self.display2.set_image(self.empty_image)
                        self.display2.write_display()

                if self.use_display3:
                    if display3_index >= -1 and display3_index < len(self.images):
                        self.display3.set_image(self.images[display3_index])
                        self.display3.write_display()
                    else:
                        self.display3.set_image(self.empty_image)
                        self.display3.write_display()

                if self.use_display4:
                    if display4_index >= -1 and display4_index < len(self.images):
                        self.display4.set_image(self.images[display4_index])
                        self.display4.write_display()
                    else:
                        self.display4.set_image(self.empty_image)
                        self.display4.write_display()

                display1_index += 1
                display2_index += 1
                display3_index += 1
                display4_index += 1
                time.sleep(self.scroll_delay) #this time governs the speed of the scroll

            # if the param is passed in, consider it an override for the class level
            # this section governs the time between scrolling messages
            time.sleep(self.repeat_delay)

    def get_starting_x_position(self,message):
        im = Image.new("1", (8*self.num_displays, 8), "black")
        draw = ImageDraw.Draw(im)
        width, ignore = draw.textsize(message, font=self.font)
        x_offset = math.floor(((8*self.num_displays) - width) / 2)

        return x_offset

    def display_message(self, message, align='Center', x_position=None):
        im = Image.new("1", (8*self.num_displays, 8), "black")

        draw = ImageDraw.Draw(im)
        #width, ignore = self.font.getsize(message)
        width, ignore = draw.textsize(message, font=self.font)

        if width > (8*self.num_displays):
            print("Message does not fit in displays: " + str(width) + "," + str(8*self.num_displays))
            return

        if x_position is None:
            if align is 'Left':
                x_offset = 0
            elif align is 'Center':
                x_offset = math.floor(((8*self.num_displays) - width) / 2)
        else:
            x_offset = x_position

        # draw the text in an image rectangle the size of all of the display
        # led packs.
        # coordinates are those of the box.
        # x1,y1,x2,y2
        # x1,y1 are upper left corner
        # x2,y2 are lower right corner
        draw.rectangle((0, 0, 7*self.num_displays, 7), outline=0, fill=0)
        draw.text((x_offset, 1), message, 1, font=self.font)

        # crop out the image for each of the displays
        start_x = 0
        height = 8
        display_width = 8
        end_x = start_x + display_width
        # crop(x,y,w,h)
        if self.num_displays >= 1:
            #im.crop((start_x, 0, end_x, 7)).save("./images/display1_image.jpg", "JPEG")
            #print("Crop size: " + str(im.crop((start_x, 0, end_x, 8)).size))
            self.display1.set_image(im.crop((0, 0, 8, 8)).rotate(90))
            self.display1.write_display()

        if self.num_displays >= 2:
            start_x = end_x+1
            end_x = start_x + width
        #    im.crop((start_x, 0, end_x, 7)).save("./images/display2_image.jpg", "JPEG")
            #print("display2 crop size: " + str(im.crop((8, 0, width-16, 8)).size))
            self.display2.set_image(im.crop((8, 0, 16, 8)).rotate(90))
            self.display2.write_display()

        if self.num_displays >= 3:
            start_x = end_x+1
            end_x = start_x + width
        #    im.crop((start_x, 0, end_x, 7)).save("./images/display3_image.jpg", "JPEG")
            self.display3.set_image(im.crop((16, 0, 24, height)).rotate(90))
            self.display3.write_display()

        if self.num_displays >= 4:
            start_x = end_x+1
            end_x = start_x + width
        #    im.crop((start_x, 0, end_x, 7)).save("./images/display4_image.jpg", "JPEG")
            self.display4.set_image(im.crop((24, 0, 32, height)).rotate(90))
            self.display4.write_display()

if __name__ == '__main__':
    matrix = MultiMatrix8x8Display(display2_address=0x74,display3_address=None,display4_address=None)
    matrix.num_displays = 2
    matrix.rotate_text = False
    matrix.scroll_message("Show on multiple 8x8 matrix displays", -1, 2)

