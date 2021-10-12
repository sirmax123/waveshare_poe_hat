import logging
import sys
import time
import smbus
import RPi.GPIO as GPIO
import os
import socket
import subprocess
import fcntl
import struct
import netifaces

from PIL import Image,ImageDraw,ImageFont
from . import SSD1306




dir_path = os.path.dirname(os.path.abspath(__file__))


#font = ImageFont.truetype(dir_path+'/Courier_New.ttf',16)
#font = ImageFont.truetype(dir_path+'/04B_08__.ttf',10)
#font = ImageFont.truetype(dir_path+'/Font.ttf',12)


class POE_HAT_B:
    def __init__(self, address = 0x20, font_size = 12, font_name='Font.ttf',
                 start_x_position = 0, start_y_position = -1, string_height_in_pixels=9,
                 interface = 'eth0'):
        self.fan_pixels_offset = 64
        self.interface = interface
        self.start_x_position = start_x_position
        self.start_y_position = start_y_position
        self.string_height_in_pixels = string_height_in_pixels
        self.i2c = smbus.SMBus(1)
        self.address = address#0x20
        self.FAN_ON()
        self.FAN_MODE = 0;
        self.font = ImageFont.truetype(dir_path+'/'+font_name, font_size)

        self.screen128_32_SSD1306 = SSD1306.SSD1306()
        self.screen128_32_SSD1306.Init();

    def FAN_ON(self):
        self.i2c.write_byte(self.address, 0xFE & self.i2c.read_byte(self.address))

    def FAN_OFF(self):
        self.i2c.write_byte(self.address, 0x01 | self.i2c.read_byte(self.address))

    def GET_IP(self):
       return netifaces.ifaddresses(self.interface)[netifaces.AF_INET][0]['addr']

    def GET_Temp(self):
        with open('/sys/class/thermal/thermal_zone0/temp', 'rt') as f:
            temp = (int)(f.read() ) / 1000.0
        return temp


    def GET_Hostname(self):
      return str(os.uname().nodename)

    def POE_HAT_Display(self, FAN_TEMP):
        # show.Init()
        self.screen128_32_SSD1306.ClearBlack()
        image = Image.new('1', (self.screen128_32_SSD1306.width, self.screen128_32_SSD1306.height), "WHITE")
        draw = ImageDraw.Draw(image)

        ip = self.GET_IP()
        temp = self.GET_Temp()
        hostname = self.GET_Hostname()

        x = self.start_x_position
        y = self.start_y_position
        draw.text((x,y), 'ip: '+str(ip),                       font = self.font, fill = 0)
        y = y + self.string_height_in_pixels
        draw.text((x,y), 'T:  '+ str(((int)(temp*10))/10.0), font = self.font, fill = 0)
        y_temp = y
        y = y + self.string_height_in_pixels
        draw.text((x,y), '' + hostname,              font = self.font, fill = 0)
        y = y + self.string_height_in_pixels

        if(temp>=FAN_TEMP):
            self.FAN_MODE = 1

        elif(temp<FAN_TEMP-2):
            self.FAN_MODE = 0

        if(self.FAN_MODE == 1):
            draw.text((x + self.fan_pixels_offset, y_temp), 'FAN:ON', font = self.font, fill = 0)
            self.FAN_ON()
        else:
            draw.text((x + self.fan_pixels_offset,y_temp), 'FAN:OFF', font = self.font, fill = 0)
            self.FAN_OFF()

        self.screen128_32_SSD1306.ShowImage(self.screen128_32_SSD1306.getbuffer(image))







