#!/usr/bin/env python3

import time
import sys
import os
import logging

libdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)

#print(os.path.realpath(__file__))
#print(os.path.dirname(os.path.realpath(__file__)))

from waveshare_POE_HAT_B import POE_HAT_B

try:
  interface = os.environ['INTERFACE']
except:
  print("Using default interface: eth0")
  interface = 'eth0'

logging.basicConfig(level=logging.INFO)
#Font.ttf
#Courier_New.ttf
#
POE = POE_HAT_B.POE_HAT_B(font_size=12, font_name='Courier_New.ttf', string_height_in_pixels=10,  interface=interface)
try:
    while(1):
        POE.POE_HAT_Display(FAN_TEMP=25)
        time.sleep(60)

except KeyboardInterrupt:
    print("ctrl + c:")
    POE.FAN_OFF()
