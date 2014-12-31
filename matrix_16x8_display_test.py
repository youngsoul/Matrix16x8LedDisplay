__author__ = 'youngsoul'

import Matrix16x8TTF

matrix = Matrix16x8TTF(font_path="/home/pi/dev/MatrixDisplay/fonts/PressStart2P.ttf", brightness=1,repeat_delay=0, scroll_delay=0.02, rotate_text=False)

matrix.scroll_message(display_message="The quick brown fox jumps over the lazy dog", num_scrolls=-1)

