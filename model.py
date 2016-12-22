import sys
import os.path
import imghdr
import PIL.Image
import PIL.ImageDraw as ImageDraw
import math
import pint
import time
from copy import deepcopy
from tkinter import *
import operator
# Class cell_analysis:
#-update analysis to work with s > r
#-update analysis to work with unit_cell class
# Class unit cell:
# confirm that filling in circles is done right
class unit_cell:
    def __init__(self, container):
        self.__define_vars(container)
        self.__create_cell()

    def __define_vars(self,container):
        self.r  = container.get_dict_value("radius")
        self.p  = container.get_dict_value("is_positive")
        self.s  = container.get_dict_value("separation")
        circ = 1
        back = 0
        if self.p is False:
            circ ^= 1
            back ^= 1

        self.circle = (0,0,0,circ*255)
        self.img_alpha = (0,0,0,back*255)
        print(str(self.circle) + "alpha" + str(self.img_alpha) + " p:" + str(self.p))
        self.__define_mask()

    def __define_mask(self):
        sep      = self.s*math.sqrt(2)  #
        self.subdiv  = int(round(sep,0))
        self.mask = PIL.Image.new('RGBA', (self.subdiv*2,self.subdiv*2), self.img_alpha)

    def __create_cell(self):
        r = self.r
        s = self.subdiv
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

    def get_image(self):
        temp = PIL.Image.new('RGBA', (self.subdiv*2,self.subdiv*2),0)
        return PIL.Image.alpha_composite(temp, self.mask)

class cell_analysis:
    def __init__(self, container):
        self.__set_values__(var_dict)

    def __set_values__(self,container):
        self.unit_cell = unit_cell(var_dict)
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

class image_vars:
    def __init__(self,var_dict):
        self.ureg = pint.UnitRegistry()
        self.default = dict(height=("2","cm"),\
                        width=("2","cm"),\
                        px_cm=("300","cm"),\
                        input_file=None,\
                        is_positive=False,\
                        separation=("0.1","cm"),\
                        radius=("0.01","cm"))
        self.__set_values(self.default)
        if self.default != None:
            self.__set_values(var_dict)

    def __set_values(self,dictionary_input):
        px_cm_conversion =   float(self.__normalize_unit(dictionary_input.get("px_cm")))
        self.default=dict( \
        height=int(int(self.__normalize_unit(dictionary_input.get("height")))*px_cm_conversion), \
        width=int(int(self.__normalize_unit(dictionary_input.get("width")))*px_cm_conversion), \
        separation=float(self.__normalize_unit(dictionary_input.get("separation")))*px_cm_conversion,\
        radius=float(self.__normalize_unit(dictionary_input.get("radius")))*px_cm_conversion,\
        is_positive=dictionary_input.get("is_positive"))

    def __normalize_unit(self,dict_val):
        return str(self.ureg(dict_val[0] + dict_val[1]).to("cm").magnitude)

    def get_dict_value(self,dict_value):
        return self.default.get(dict_value)

def createpng(container):
    var_list = __define_vars(container)
    return __create_png_from_vars(var_list)

def __define_vars(container):
    separation     = container.get_dict_value("separation")
    cell      = unit_cell(container)
    dimensions = (container.get_dict_value("height"),container.get_dict_value("width"))
    input_file          = container.get_dict_value("input_file")
    if input_file == None:
        img = PIL.Image.new('RGBA', (dimensions[0],dimensions[1]), 255)
    else:
        img = PIL.Image.open(input_file.get())
        img = img.convert("RGBA")
        img = img.resize((dimensions[0],dimensions[1]))
    return dict(separation=separation, \
                unit_cell= cell,  \
                dimensions=dimensions, \
                image=img)

def __create_png_from_vars(var_list):
    ## need a dummy image, mask, and
    dim  = var_list.get("dimensions")
    tile_mask = var_list.get("unit_cell").get_mask()
    tilewidth, tileheight = tile_mask.size
    mask = PIL.Image.new('RGBA', (dim[0], dim[1]),255)
    for left in range(0, dim[0], tilewidth):
        for top in range(0, dim[1], tileheight):
              mask.paste(tile_mask, (left, top))

    return PIL.Image.alpha_composite(var_list.get("image"), mask)
