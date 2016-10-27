import sys
import os.path
import imghdr
import PIL.Image
import math
import time
from copy import deepcopy
from tkinter import *

class png_maker:
    def __init__(self, container):
        #self.root.mainloop()
        self.circles        = []
        self.r              = container.get_radius()
        self.x              = container.get_width_pixels()
        self.y              = container.get_height_pixels()
        self.positive       = container.get_positive()
        self.separation     = container.get_separation()
        if container.image_file == None:
            img = PIL.Image.new('RGBA', (self.x,self.y), 0)
        else:
            img = PIL.Image.open(input_file)
            img = img.convert("RGBA")
        self.img = img

    def createpng(self):
        '''creates a png with specified holes'''
        self.__initcircles()
        self.__initalphamask()
        self.__drawcircles()
        return self.img


    def __initcircles(self):
        '''creates a short list of cirlce tuple coordinates'''
        # this function creates a list of 2d tuples storing pixels inside a circle
        # to do that, it scans from x = 0 -> circle radius, evaluating if the relation
        # x^2 + y^2 < rad^2 holds true. If so, it adds the following points to a
        # circle point list:
        # ( x,y ) Quadrant 1.
        # (-x,y ) Quadrant 2.
        # (-x,-y) Quadrant 3.
        # ( x,-y) Quadrant 4.

        circleRadius = int(self.r)
        circleRadiusSquared = circleRadius*circleRadius
        for x in range(circleRadius):
            ybase = 0
            while (ybase*ybase + x*x) <= circleRadiusSquared:
                self.circles.append((x,ybase))
                self.circles.append((-x,ybase))
                self.circles.append((-x,-ybase))
                self.circles.append((x,-ybase))
                ybase=ybase+1

    def __initalphamask(self):
        ''' Puts an alpha mask of 0 or 1 across the image,
        depending on input parameters'''
        pixdata = self.img.load()

        if self.positive:
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
        sep        = self.separation
        root2       = 1/(math.sqrt(2))

        x_1         = sep*root2
        x_i         = sep*root2*2
        y_1         = sep*root2
        y_i         = sep*root2*2

        xwidth      = self.x
        yheight     = self.y

        # dividing total pixel length on one side by the width of the iterator
        # gives us the expected number of iterations per raster scan.
        dimensions  = (xwidth,yheight)
        x_f         = int(xwidth/x_i)
        y_f         = int(yheight/y_i)
        # *********************************************************
        # ******************* Extraneous Loop things **************

        # tells us whether the alpha value should be zero or not
        if self.positive:
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

class image_vars:
    def __init__(self):

        self.conversionFactor = 1
        self.is_positive=True
        self.separation=200
        self.radius=70
        self.dimensions = [100,100]
        self.image_file = None

    #sets the input file path. imgFile input is path
    def set_image_file(self,imgFile):
        msg =  None
        if imgFile is None:
            self.image_file = None

        else:
            if os.path.isfile(imgFile):
                if os.access(imgFile, os.R_OK):
                    if imghdr.what(imgFile)=='png':
                        self.image_file=imgFile

                    else:
                        msg= "Looks like input file is type " +imghdr.what(self.pngFilePath) \
                         + "\n Please use input image of type png!"

                else:
                    msg="Warning! File does not have access permissions"

            else:
                msg="File seems to be missing! Maybe path is incorrect?"

        return msg

    #sets the desired dimensions in px units
    def set_height(self,dim):
        """sets the desired dimensions in px units"""
        self.dimensions[1] = dim

    def set_width(self,dim):
        """sets the desired dimensions in px units"""
        self.dimensions[0] = dim

    #sets whether a print is positive or negative
    def set_positive(self,pos):
        """determines what kind of image to produce"""
        self.is_positive = pos

    #sets the dot separation width (cen1->cen2) in cm
    def set_separation(self,sep):
        self.separation = sep

    #sets circle radius in cm
    def set_radius(self,rad):
        self.radius = rad

    #gets the img file path
    def get_image_file(self):
        return self.image_file

    #gets the print width in pixels
    def get_width(self):
        return self.dimensions[0]

    #gets the print height in pixels
    def get_height(self):
        return self.dimensions[1]

    #returns whether the print should be positive or not
    def get_positive(self):
        return self.is_positive

    #gets the cirlce/dot separation in px
    def get_separation(self):
        return self.separation

    #gets the cirlce/dot radius in px
    def get_radius(self):
        return self.radius
