###############################################################
#                                                             #
#                      P I C O P L A S M A                    #
#                                                             #
#  Raspberry Pi Pico                                          #
#  Pimoroni Pico Unicorn Pack                                 #
#                                                             #
#  2021 by signheim                                           #
#                                                             #
#  Learned and modified plasma algorhithms from two sources:  #
#  https://www.bidouille.org/prog/plasma                      #
#  https://rosettacode.org/wiki/Plasma_effect#Python          #
#                                                             #
###############################################################

import picounicorn
import math

def grey_to_rainbow(h): # simplified hsv_to_rgb (s and v are always 1 in a rainbow)
    i = int(h * 6)
    f = 1 - (h * 6 - i)
    t = 1 - f
    i %= 6
    if i == 0: return 1, t, 0
    if i == 1: return f, 1, 0
    if i == 2: return 0, 1, t
    if i == 3: return 0, f, 1
    if i == 4: return t, 0, 1
    if i == 5: return 1, 0, f

picounicorn.init() # setting up the picounicorn
w = picounicorn.get_width()
h = picounicorn.get_height()

t = 0     # kind of time variable (without time)
ti = 0.1  # increment for the time
ap = 0    # debouncers for the buttons (BUTTON_B doesn't need it)
yp = 0
xp = 0
cm = 0    # the color mode, can be 0 (polychrome) or 1 (monochrome)
ca = 0    # the color arrangement, can be 0, 1 or 2


def pix(x, y): # plasma function
    v = 4
    v += math.sin((x - t) / 1.5)
    v += math.sin((y + t) / 1.5)
    v += math.sin((x - y + t) / 2)
    x += math.sin(t / 5) / 2
    y += math.cos(t / 3) / 2
    v += math.sin((math.sqrt(x ** 2 + y ** 2 + 1) + t) / 2)
    v /= 8
    if cm == 0: r, g, b = grey_to_rainbow(v) # polychrome
    elif cm == 1:                            # monochrome
        if ca == 0: r, g, b = v, v, v
        elif ca == 1: r, g, b = v, v / 2, v / 4
        elif ca == 2: r, g, b = v / 2, v, v / 4
    if ca == 0: return int(r * 255), int(g * 255), int(b * 255)  # cycle r, g and b
    elif ca == 1: return int(b * 255), int(r * 255), int(g * 255)
    elif ca == 2: return int(g * 255), int(b * 255), int(r * 255)

while True:
    t += ti
    if t >= 12 * math.pi: t = 0 # cycle repeats after 12*pi, t doesn't neet to grow forever
    
    for x in range(w):
        for y in range(h):
            r, g, b = pix(x, y)                  # calculating color
            picounicorn.set_pixel(x, y, r, g, b) # setting color to LED
    
    if picounicorn.is_pressed(picounicorn.BUTTON_A): # slow, medium, fast, slow, ...
        if ap == 0:
            if ti == 0.1: ti = 0.2
            elif ti == 0.2: ti = 0.4
            elif ti == 0.4: ti = 0.1
            ap = 1
    else: ap = 0
    
    if picounicorn.is_pressed(picounicorn.BUTTON_B): # stop while pressed
        t -= ti
        
    if picounicorn.is_pressed(picounicorn.BUTTON_X): # mono or poly
        if xp == 0:
            if cm == 0: cm = 1
            elif cm == 1: cm = 0
            xp = 1
    else: xp = 0
    
    if picounicorn.is_pressed(picounicorn.BUTTON_Y): # color change
        if yp == 0:
            if ca == 0: ca = 1
            elif ca == 1: ca = 2
            elif ca == 2: ca = 0
            yp = 1
    else: yp = 0