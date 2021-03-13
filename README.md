# PICOPLASMA
Plasma Generator for Raspberry Pi Pico with Pimoroni Unicorn Pack

Based mainly on two great contributions about the plasma-effect
  - https://www.bidouille.org/prog/plasma
  - https://rosettacode.org/wiki/Plasma_effect#Python

How it works
------------
Power up the Pi Pico with the Pimoroni Unicorn Pack installed.
Plasma will immediately start on the LED matrix.

Press A to cycle through 3 speeds
Press B to hold the animation
Press C to switch polychrome and monochrome
Press D to cycle through 3 color modes

Enjoy!

Code preparations
-----------------
To get access to Pimoronis product specific librarys the Pi Pico
needs to be flashed with a Package from Pimoroni that has
the usual MicroPython on board plus the librarys for the
Unicorn Pack and other stuff from Pimoroni.
  - https://github.com/pimoroni/pimoroni-pico/releases

Save the 'picoplasma.py' as 'main.py'
to the Pico to enable it without computer
connection.

Parts
-----
  - Raspberry Pi Pico
  - Pimoroni Unicorn Pack
    - https://shop.pimoroni.com/products/pico-unicorn-pack

Wiring
------
The Pimoroni Unicorn Pack is designed for a direct connection with the Pi Pico.
If the Pico has pins soldered the usual way the Pack fits on it's back and is
wired automatically.
