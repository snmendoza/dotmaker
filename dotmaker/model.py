import sys
import os.path
import imghdr
import PIL.Image
import math
import pint
import time
from copy import deepcopy
from tkinter import *

class png_maker:
    def __init__(self, container):
        self.circles        = []
        self.r              = container.get_radius()
        self.x              = container.get_width()
        self.y              = container.get_height()
        self.positive       = container.get_positive()
        self.separation     = container.get_separation()
        input_file          = container.get_image_file()

        if input_file == None:
            img = PIL.Image.new('RGBA', (self.x,self.y), 0)
        else:
            img = PIL.Image.open(input_file.get())
            img = img.convert("RGBA")
            img = img.resize((self.x,self.y))
        self.img = img

    def get_img_obj(self):
        cont_dict = dict(image = self.img,
                         separation = self.separation,
                         radius = self.r,
                         positive = self.positive)
        container = image_container(cont_dict)
        return container

    def createpng(self):
        '''creates a png with specified holes'''
        self.__initcircles()
        self.__initalphamask()
        self.__drawcircles()

    def __initcircles(self):
        '''creates a short list of cirlce tuple coordinates'''
        r = int(self.r)
        x = r
        y = 0
        p = 1 - r
        while x >= y:
            self.__circle_param_set(x,y)
            y=y+1
            if p < 0:
                p = p + 2*y + 1

            else:
                x = x - 1
                p = p + 2*(y-x) + 1


    def __circle_param_set(self,x,y):
        #octants 1,4,5,8
        for i in range(0,x+1):
            self.__circle_set(( x - i, y))
            self.__circle_set((-x + i, y))
            self.__circle_set((-x + i,-y))
            self.__circle_set(( x - i,-y))
        #octants 2,3,6,7
        for i in range(0,y+1):
            self.__circle_set(( y-i, x))
            self.__circle_set((-y+i, x))
            self.__circle_set((-y+i,-x))
            self.__circle_set(( y-i,-x))

    def __circle_set(self,tup):
        if tup not in self.circles:
            self.circles.append(tup)

    def __initalphamask(self):
        ''' Puts an alpha mask of 0 or 1 across the image,
        depending on input parameters'''
        pixdata = self.img.load()

        if self.positive==True:
            alpha = 0
        else:
            alpha = 255

        for y in range(self.y):
            for x in range(self.x):
                pixdata[x, y] = \
                    (pixdata[x,y][0],pixdata[x,y][1], pixdata[x,y][2], alpha)

    def __drawcircles(self):
        '''places circles across the alpha layer of the png'''
        # This function raster scans across the png image
        # There are two types of scans.
        # One starts at 0,0 and iterates up x and y by iterator 2*separation/sqrt(2)
        # The second starts at separation/sqrt(2), separation/sqrt(2) and iterates
        # up x and y by 2*separation/sqrt(2)
        # The 2/root(2) comes from geometry relations between the circle centers
        # ******************* Iterator variables ******************
        sep         = self.separation
        xwidth      = self.x
        yheight     = self.y

        x_1         = sep*math.sqrt(2)/2
        y_1         = sep*math.sqrt(2)/2

        x_i         = sep*math.sqrt(2)
        y_i         = sep*math.sqrt(2)

        # dividing total pixel length on one side by the width of the iterator
        # gives us the expected number of iterations per raster scan.
        dimensions  = (xwidth,yheight)
        x_f         = int(xwidth/x_i)
        y_f         = int(yheight/y_i)
        # *********************************************************
        # ******************* Extraneous Loop things **************

        # tells us whether the alpha value should be zero or not
        if self.positive==True:
            alpha = 255
        else:
            alpha = 0

        pxDat = self.img.load()
        for x in range(x_f+1):
            for y in range(y_f+1):
                # Get the list of valid circle points per iterator position
                # Remember that there are two different types of rows here
                centerCoordinate00 = (int(x*x_i),int(y*y_i))
                centerCoordinater2r2 = (int(x_1+(x*x_i)),int(y_1+(y*y_i)))
                circleList00 = \
                    self.__getAdjustedPoints(centerCoordinate00,dimensions)
                circleListr2r2 = \
                    self.__getAdjustedPoints(centerCoordinater2r2,dimensions)
                for i in range(len(circleList00)):
                    place = circleList00[i]
                    temppx = pxDat[place[0],place[1]]
                    pxDat[place[0],place[1]] = \
                        (temppx[0],temppx[1],temppx[2],alpha)

                for i in range(len(circleListr2r2)):
                    place = circleListr2r2[i]
                    temppx = pxDat[place[0],place[1]]
                    pxDat[place[0],place[1]] = \
                        (temppx[0],temppx[1],temppx[2],alpha)

    def __getAdjustedPoints(self,centerCoordinate,dimensions):
        '''Adjusts each point within the circle list
        to have a center around given coordinates'''
        # This function takes the list of circle points and offsets them via
        # the given x,y coordinate. Also passes the xwidth and y width to ensure
        # only circle pixels within the frame are passed
        c_x = centerCoordinate[0]
        c_y = centerCoordinate[1]
        newlist = []

        if  c_x  - (self.r)>= 0 and self.r + c_x < dimensions[0] \
        and c_y -  (self.r)>=0  and self.r + c_y < dimensions[1]:
            for i in range(0,len(self.circles)):
                circlepoint = self.circles[i]
                xadj = circlepoint[0] + c_x
                yadj = circlepoint[1] + c_y
                newlist.append((xadj,yadj))

        else:
            for i in range(0,len(self.circles)):
                circlepoint = self.circles[i]
                xadj = circlepoint[0] + c_x
                yadj = circlepoint[1] + c_y
                if xadj in range(dimensions[0]) and yadj in range(dimensions[1]):
                    newlist.append((xadj,yadj))

        return newlist

class image_container:
    def __init__(self, var_dict):
        self.__set_values__(var_dict)

    def __set_values__(self,var_dict):
        self.__img = var_dict.get("image")
        self.__sep = var_dict.get("separation")
        self.__radius = var_dict.get("radius")
        self.__pos = var_dict.get("positive")

    def get_image(self):
        return self.__img.copy()

    def get_unit_image(self):
        temp_img = self.get_image()
        xdim = int(math.sqrt(2)*self.__sep+1)
        ydim = xdim
        return temp_img.crop((0,0,xdim,ydim))

    def get_theoretical_opacity(self):
        r = self.__radius
        s = self.__sep
        s2 = float(s*s)
        r2 = float(r*r)
        if 2*r < s:
            if self.__pos == True:
                print("positive")
                return math.pi*r2 / s2

            else:
                print("negative")
                return ((s2 - math.pi*r2) / s2)

        else:
            return 0.99;


    def get_numerical_opacity(self):
        temp_img = self.get_unit_image()
        xdim = int(math.sqrt(2)*self.__sep)
        ydim = xdim
        alpha = 0
        for x in range(0,xdim+1):
            for y in range(0,ydim+1):
                pixel_tuple = temp_img.getpixel((x,y))
                alpha = alpha + pixel_tuple[3]

        return alpha / (255*xdim*ydim)

class image_vars:
    def __init__(self,var_dict):
        self.dimensions=dict(height=100,width=100)
        self.is_positive=False
        self.radius = 1
        self.separation = 1
        self.img_file = None
        self.dict = var_dict
        self.ureg = pint.UnitRegistry()
        self.default = dict(height=("2","cm"),\
                        width=("2","cm"),\
                        px_cm=("300","cm"),\
                        input_file=None,\
                        is_positive=False,\
                        separation=("0.1","cm"),\
                        radius=("0.01","cm"))
        self.__set_values(self.default)
        if self.dict != None:
            self.__set_values(self.dict)


    def __set_values(self,dictionary_input):
        px_cm_conversion =   int(self.normalize_unit(dictionary_input.get("px_cm")))
        self.set_height(     float(self.normalize_unit(dictionary_input.get("height")))*px_cm_conversion)
        self.set_width(      float(self.normalize_unit(dictionary_input.get("width")))*px_cm_conversion)
        self.set_separation( float(self.normalize_unit(dictionary_input.get("separation")))*px_cm_conversion)
        self.set_radius(     float(self.normalize_unit(dictionary_input.get("radius")))*px_cm_conversion)

        self.set_image_file( dictionary_input.get("input_file"))
        self.set_positive(   dictionary_input.get("is_positive"))

    def normalize_unit(self,dict_val):
        return str(self.ureg(dict_val[0] + dict_val[1]).to("cm").magnitude)
    #sets the input file path. imgFile input is path
    def set_image_file(self,imgfile):
        self.imgfile=imgfile
    #sets the desired dimensions in px units
    def set_height(self,dim):
        self.dimensions["height"] = int(dim)

    def set_width(self,dim):
        """sets the desired dimensions in px units"""
        self.dimensions["width"] = int(dim)

    #sets whether a print is positive or negative
    def set_positive(self,pos):
        """determines what kind of image to produce"""
        self.is_positive = pos

    #sets the dot separation width (cen1->cen2) in cm
    def set_separation(self,sep):
        self.separation = int(sep)

    #sets circle radius in cm
    def set_radius(self,rad):
        self.radius = int(rad)

    #gets the img file path
    def get_image_file(self):
        return self.imgfile
    #gets the print width in pixels
    def get_width(self):
        return self.dimensions.get("width")

    #gets the print height in pixels
    def get_height(self):
        return self.dimensions.get("height")

    #returns whether the print should be positive or not
    def get_positive(self):
        return self.is_positive

    #gets the cirlce/dot separation in px
    def get_separation(self):
        return self.separation

    #gets the cirlce/dot radius in px
    def get_radius(self):
        return self.radius
