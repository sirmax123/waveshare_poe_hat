from smbus import SMBus
import time
import pprint
#import numpy as np
#128 × 32
class SSD1306(object):
    def __init__(self, width=128, height=32, addr=0x3c):
        self.width = width
        self.height = height
        self.Column = width
        self.Page = int(height/8)
        self.addr = addr
        self.bus = SMBus(1)

    def SendCommand(self, cmd):# write command
        self.bus.write_byte_data(self.addr, 0x00, cmd)

    def SendData(self, cmd):# write ram
        self.bus.write_byte_data(self.addr, 0x40, cmd)

    def Closebus(self):
        self.bus.close()

    def Init(self):
        self.SendCommand(0xAE)

        self.SendCommand(0x40) # set low column address
        self.SendCommand(0xB0) # set high column address

        self.SendCommand(0xC8) # not offset

        self.SendCommand(0x81)
        self.SendCommand(0xff)

        self.SendCommand(0xa1)

        self.SendCommand(0xa6)

        self.SendCommand(0xa8)
        self.SendCommand(0x1f)

        self.SendCommand(0xd3)
        self.SendCommand(0x00)

        self.SendCommand(0xd5)
        self.SendCommand(0xf0)

        self.SendCommand(0xd9)
        self.SendCommand(0x22)

        self.SendCommand(0xda)
        self.SendCommand(0x02)

        self.SendCommand(0xdb)
        self.SendCommand(0x49)

        self.SendCommand(0x8d)
        self.SendCommand(0x14)

        self.SendCommand(0xaf)

    def ClearBlack(self):
        for i in range(0, self.Page):
            self.SendCommand(0xb0 + i)
            self.SendCommand(0x00)
            self.SendCommand(0x10) 
            for j in range(0, self.Column):
                self.SendData(0x00)
#                self.SendData(0x33)

    def ClearWhite(self):
        for i in range(0, self.Page):
            self.SendCommand(0xb0 + i)
            self.SendCommand(0x00)
            self.SendCommand(0x10) 
            for j in range(0, self.Column):
                self.SendData(0xff)

    def getbuffer(self, image):
        buf = [0xff] * (self.Page * self.Column)
        image_monocolor = image.convert('1')
        imwidth, imheight = image_monocolor.size
        pixels = image_monocolor.load()


#        for j in range(0, imheight):
#            print("{:02d}".format(j), end=' ')
#            for i in range(0, imwidth):
#                if (pixels[i, j] == 255):
#                   print(" ", end='')
#                else:
#                   print("#", end='');
#            print("")
#
        if(imwidth == self.width and imheight == self.height):
            # print ("Horizontal screen")
            for y in range(imheight):
                for x in range(imwidth):
                    # Set the bits for the column of pixels at the current position.
                    if pixels[x, y] == 0:
# Буффер который нужно будет записать организован постранично
# Первая страница - это первые 8 строк, вотрая - вторые 8 строк и так далее
# При этом нулевой байт первой страницы отвечает за 8 пикселей по вертикали -
# [x=0, y=0] [x=0, y=1] [x=0, y=2] ... [x=0, y=7]
# Первый байт первой страницы соответвенно за
# [x=1, y=0] [x=1, y=1] [x=1, y=2] ... [x=1, y=7]
# и так далее до x=127
#
# Вторая страница - это следующие 8 строк, нулевой байт -
# [x=0, y=8] [x=0, y=9] [x=0, y=10] ... [x=0, y=15]
# и так далее остальные страницы
#
# Соответвенно что бы сформировать такой буффер 
# (x + int(y / 8 ) * self.width)
# Для первых 8 строк (0 - 7)  int(y/8) = 0  т.е. адрес определяется только X
# Для следующих 8 строк - к адресу прибавляется смещение в 128 т е массив будет заполнятся
# со смещением в 128 для каждой строки
#
# Значение  - это адрес пикселя ПО ВЫСОТЕ от 0 до 7
# 1 << (y % 8)  означает "сдвинуть 1 на остаток от деления на 8
# Смысл этого действия - выставить в 1 бит соответвующий адресу пикселя по вертикали
# в байте буфера (&= -  надожение масеи по-месту, если нужный бит не выствлен - он будет установлен
# в правильное значение, при этом остальные биты не будут модифицироваться
                        buf[x + int(y / 8) * self.width] &= ~(1 << (y % 8))

        elif(imwidth == self.height and imheight == self.width):
            # print ("Vertical screen")
            for y in range(imheight):
                for x in range(imwidth):
                    newx = y
                    newy = self.height - x - 1
                    if pixels[x, y] == 0:
                        buf[(newx + int(newy / 8 )*self.width) ] &= ~(1 << (y % 8))

        for x in range(self.Page * self.Column):
            buf[x] = ~buf[x]
        return buf





    def ShowImage(self, pBuf):
        for i in range(0, self.Page):
            self.SendCommand(0xB0 + i) # set page address
            self.SendCommand(0x00)     # set low column address
            self.SendCommand(0x10)     # set high column address
            # write data #
            for j in range(0, self.Column):
            # 0 .. 127
                self.SendData(pBuf[j+self.width*i])

