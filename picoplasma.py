####################################################################
#                                                                  #
#                        P I C O P L A S M A                       #
#                      W I T H   M E S S A G E                     #
#                                                                  #
#  Raspberry Pi Pico                                               #
#  Pimoroni Pico Unicorn Pack                                      #
#                                                                  #
#  2021 by signheim                                                #
#                                                                  #
#  Learned and modified plasma algorhithm from two sources:        #
#  https://www.bidouille.org/prog/plasma                           #
#  https://rosettacode.org/wiki/Plasma_effect#Python               #
#                                                                  #
#  Took my first steps into framebuffering with the help of:       #
#  https://github.com/harveysandiego/raspberry_pi_pico_micropython #
#                                                                  #
#  rainbow_colors(h) is a simplified version of                    #
#  CPythons colorsys module's hsv_to_rgb converter                 #
#  (for in a rainbow s and v are always 1)                         #
#                                                                  #
####################################################################

import picounicorn
import math
import framebuf

picounicorn.init() # setting up the picounicorn
w = picounicorn.get_width()
h = picounicorn.get_height()

t = 0      # kind of time variable (don't need utime module, calculations make the pico slow enough)
ti = 0.15  # increment for the time
db = False # debouncer for the buttons
cm = 0     # the color mode, can be 0 (polychrome) or 1 (monochrome)
tm = 1     # text mode
wm = 0     # which message
fbw = 0    # framebuffer width
fc = -10   # framebuffer counter for scrolling an renewing

# Array with all messages, you can add as many as you like
mes = ['Picoplasma',
       'by signheim']

# Projects greyscale-values to rainbow-colors
def rainbow_color(h):
    i = int(h * 6)
    f1 = 1 - (h * 6 - i)
    f2 = 1 - f1
    i %= 6
    if i == 0: return          255 , int(f2 * 255),            0
    if i == 1: return int(f1 * 255),          255 ,            0
    if i == 2: return            0 ,          255 , int(f2 * 255)
    if i == 3: return            0 , int(f1 * 255),          255
    if i == 4: return int(f2 * 255),            0 ,          255
    if i == 5: return          255 ,            0 , int(f1 * 255)

# Calculates the plasma-effect
def pix_color(x, y, m):
    v = 4                                                                # prevents negative values
    v += math.sin((x - t) / 1.5)                                         # first sinewave in x-direction
    v += math.sin((y + t) / 1.5)                                         # second sinewave in y-direction
    v += math.sin((x - y + t) / 2)                                       # third sinewave at an angle
    x += math.sin(t / 5) / 2                                             # changing x by time
    y += math.cos(t / 3) / 2                                             # changing y by time
    v += math.sin((math.sqrt(x ** 2 + y ** 2 + 1) + t) / 2)              # fourth sinewave, circular
    v /= 8                                                               # calculate a value from 0 to 1
    if m < 3: r, g, b = rainbow_color(v)                                 # first three color modes need rainbow-rgb
    else:     r, g, b = int(v * 255 / 4), int(v * 255 / 2), int(v * 255) # all others are monochrome
    
    if m == 0 or m == 3: return r, g, b                                  # change order of r, g and b
    if m == 1 or m == 4: return b, r, g                                  # to achieve simple but cool
    if m == 2 or m == 5: return g, b, r                                  # color effects

# creates a framebuffor for the scrolling text
def buf_maker():
    global fbw                                              # enable to manipulate a global variable
    global fb
    fbw = (len(mes[wm]) + 3) * 8                            # width of framebuffer needs to be 3 letters longer (1 letter = 8 pixel width): two letters for the
                                                            # beginning and one for the end (there are some bugs in framebuf that are prevented this way)
    fb = framebuf.FrameBuffer(bytearray(fbw * h // 8),      # creating the bytearray from width and height, but nly one bit per pixel is needed (// 8)
                              fbw,                          # the width of the framebuffer, not the width of the unicorn-display
                              h,                            # the height of the unicorn-display
                              framebuf.MONO_HMSB)           # indicates that we need only one bit per pixel in a specific order
    fb.fill(1)                                              # fill the entire frambuffer with 1-values
    fb.text(mes[wm], 16, 0, 0)                              # fill the letters of the chosen text with 0-values, so text is invers

# main loop
while True:
    
    # fc is the counter for the framebuffer-scrolling, if it reaches -10, the buf_maker function creates the framebuffer.
    # Once fb reaches 1 the framebuffer is visualized on the unicorn-display. After the whole framebuffer is scrolled through
    # fb will be resetted to -30. The minus-parts of this counter is for a wating time between the appearance of the text
    # in order to enjoy the plasma-effect before it is masked by the text. But to let it start at -30 instead of -10 the initial
    # waiting time would be too long. So whatever is set in the beginning of the code must be set here, too. I the buffer would be
    # created at 0 (which would be enough for it starts not before fb == 1) it would be missed in the display-routine below. This
    # makes sure that the framebuffer exists from the beginning.
    if fc == -10:
        buf_maker()
    fc += 1
    
    # This application doesn't need utime for a sleep because all calculations need much time and to let them just loop
    # creates a good timing. But the plasma-effect needs some time-related variable. That is t. It grows by ti (0.15 at the beginning)
    # and ti is therefore responsible for the tempo of the plasma-effect. But the sine-function-pattern starts to repeat itselt at 12 + pi.
    # Thats why t is resetted there. It would be not necessary. But if you think about letting this run for days t could be a really
    # great number that the processor would sooner or later start to struggle with in all the sine-functions.
    t += ti
    if t >= 12 * math.pi: t = 0
    
    # This loop iterates through all pixels of the unicorn-display and initiates the plasma-effect-calculation. If the text-masking of
    # the plasma-effect is active (which is the case inititally: tm == 1) the returned rgb-values are multiplied with the value
    # found in the framebuffer at this moment in scrolling. If it is 1 the color appears, if 0 the led is off (black). This is the reason
    # why the framebuffer was created with inverted text.
    for x in range(w):
        for y in range(h):
            r, g, b = pix_color(x, y, cm)
            if tm == 0:
                picounicorn.set_pixel(x, y, r, g, b)
            else:
                s = fb.pixel(x, y)
                picounicorn.set_pixel(x, y, r * s, g * s, b * s)
                
    
    # The scrolling starts at fc == 0. Two empty letter-spaces of 8 pixels each where inserted when the framebuffer was created.
    # For the unicorn-display has exactly 16 columns there is no letter visible and therefore no masking takes place.
    # After fc reaches fbw (the width of the framebuffer) the text is scrolled entirely through the screen and scrolling stops.
    # fc is then resetted to -30 and at -10 the same framebuffer will be created unless the user did not change the text.
    if fc >= 1 and fc <= fbw:
        fb.scroll(-1, 0)
    elif fc > fbw:
        fc = -30
    
    # All buttons have a simple but effective debouncing. Once they are pressed the ap (or bp, xp, yp) variable is set to True
    # and the function can not be fired again. Not before the button is released the variable is set to False again.
    
    # Button A makes the plasma-effect faster, let it stop and start it again slow in a cycle. The appliction starts with the lowest
    # tempo. Two more speeds appear and than a stop. But only the speed of the plasma-effect is affected, not the scrolling of the text.
    # Even if the plasma-effect is stopped it is calculated constantly in order to keep the animation-speed constant.
    # There are more elgant ways to keep up a constant-speed ... I know.
    if picounicorn.is_pressed(picounicorn.BUTTON_A):
        if not db:
            db = True
            ti += 0.15
            if ti > 0.46:
                ti = 0
    else: db = False
    
    # Button B iterated through the color modes: rgb, gbr, brg, mono-blueish, mono-reddish, mono-greenish
    if picounicorn.is_pressed(picounicorn.BUTTON_B):
        if not db:
            db = True
            cm += 1
            if cm > 5: cm = 0
    else: db = False
    
    # Button X switches the text-mode on and off. The framebuffer is still calculated and scrolled.
    # This keeps the animation-speed constant. There are more elgant ways to keep up a constant-speed ... I know.
    if picounicorn.is_pressed(picounicorn.BUTTON_X):
        if not db:
            db = True
            tm += 1
            if tm > 1:
                tm = 0
    else: db = False
    
    # Button Y changes the text. It cycles through all textes in the mes-array, regardless how many there are.
    # I did not test how long a text can be without slowing everything down. Would be interesting to know.
    if picounicorn.is_pressed(picounicorn.BUTTON_Y):
        if not db:
            db = True
            wm += 1
            if wm >= len(mes):
                wm = 0
    else: db = False
