import imghdr
import PIL.Image
import PIL.ImageDraw as ImageDraw
import math
from copy import deepcopy
from tkinter import *
import operator

class UnitCell:
    def __init__(self, vardict):
        self.__defineVars(vardict)
        self.__create_cell()

    def __defineVars(self,vardict):
        self.r  = vardict.get("radius")
        self.p  = vardict.get("is_positive")
        self.s  = int(round(vardict.get("separation")*math.sqrt(1/2),0))
        self.cellSize = (self.s*2+1,self.s*2+1)
        circ = 1
        back = 0
        if self.p is False:
            circ ^= 1
            back ^= 1

        self.circle = (0,0,0,circ*255)
        self.img_alpha = (0,0,0,back*255)
        self.mask = PIL.Image.new('RGBA', self.cellSize, self.img_alpha)

    def __create_cell(self):
        r = self.r
        s = self.s
        radius = (-r,-r, r, r)
        draw = ImageDraw.Draw(self.mask)
        for x in range(0,2):
            for y in range(0,2):
                b = (s*x*2,s*y*2,s*x*2,s*y*2)
                draw.ellipse(tuple(map(operator.add, radius, b)),fill=self.circle)

        b = (s,s,s,s)
        draw.ellipse(tuple(map(operator.add, radius, b)),fill=self.circle)
        del draw

    def get_mask(self):
        return self.mask.copy()

    def getImage(self):
        temp = PIL.Image.new('RGBA',self.cellSize,0)
        return PIL.Image.alpha_composite(temp, self.mask)

class Cell_analysis:
    def __init__(self, container):
        self.__set_values__(var_dict)

    def __set_values__(self,container):
        self.unit_cell = UnitCell(var_dict)
        self.r = container.get_dict_value("radius")
        self.s = container.get_dict_value("separation")

    def get_unit_image(self):
        return self.unit_cell.get_image()

    def get_theoretical_opacity(self):
        r = self.r
        s = self.s
        s2 = float(s*s)
        r2 = float(r*r)
        if 2*r < s:
            if self.__pos == True:
                return math.pi*r2 / s2

            else:
                return ((s2 - math.pi*r2) / s2)

        else:
            return 0.99;


    def get_numerical_opacity(self):
        temp_img = self.get_unit_image()
        n_i      = self.__sep*math.sqrt(2)
        width, height = temp_img.size
        alpha_sum    = 0
        for x in range(0,xdim):
            for y in range(0,ydim):
                pixel_tuple = temp_img.getpixel((x,y))
                alpha_sum = alpha_sum + pixel_tuple[3]

        return alpha / (255*xdim*ydim)

def __getPreImage(varDict):
    size = (varDict.get("width"), varDict.get("height"))
    if varDict.get("input_file") == None:
        img = PIL.Image.new('RGBA', size, (0,0,0,255))
    else:
        img = varDict["input_file"].copy()
        img = img.convert("RGBA")
        img = img.resize(size)
    return img

def createSinglePrintPng(varDict):
    ## need a dummy image, mask, and
    size = (varDict.get("width"), varDict.get("height"))
    cell = UnitCell(varDict)
    tile_mask = cell.get_mask()
    tilewidth, tileheight = tile_mask.size
    main = PIL.Image.new('RGBA', size, 255)
    m = PIL.Image.new('RGBA', size ,255)
    preimg = __getPreImage(varDict)
    for left in range(0, size[0], tilewidth):
        for top in range(0, size[1], tileheight):
              m.paste(tile_mask, (left, top),mask=tile_mask)

    main.paste(preimg,(0,0),m)
    return main
