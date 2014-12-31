__author__ = 'youngsoul'

__author__ = 'youngsoul'

import time
from fonts import custom_font


def rotateCCW(c):
    result=[0,0,0,0,0,0,0,0]
    for x in range(0,8):
        for y in range(0,8):
            #print '{0:2d} {1:2d} {2:8b} {3:0=8b}'.format(x,y,c[x],(c[x]&0x01<<y))
            result[x]=result[x] | ( (c[y] & 0x01<<x) >> x <<y)
    return result


def rotateCW(c):
    result=[0,0,0,0,0,0,0,0]
    for x in range(0,8):
        for y in range(0,8):
            result[x]=result[x] | ( (c[7-y] & 0x01<<x) >> x <<y)
    return result


rotated_font = {}
font = custom_font.shapes
print(font)
for l in font.items():
    letter = l[0]
    letter_data = l[1]
    print("l: " + str(letter))
    rotated_letter = rotateCW(letter_data)
    #rotated_letter = rotateCW(rotated_letter)
    hex_rotated_letter = []
    for z in rotated_letter:
        hex_rotated_letter.append(hex(z))
    rotated_font[letter] = hex_rotated_letter

print(rotated_font)






