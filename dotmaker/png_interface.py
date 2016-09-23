import sys
import os.path
import imghdr
import PIL.Image
import math
from containers import image_vars
from copy import deepcopy

class png_maker:
    def __init__(self, container):

        self.circles        = []
        self.r              = container.get_dot_px_radius()
        self.x              = container.get_width_pixels()
        self.y              = container.get_height_pixels()
        self.positive       = container.get_positive()
        self.separation     = container.get_dot_px_separation()

        if container.image_file == None:
            img = PIL.Image.new('RGBA', (self.x,self.y), 0)

        else:
            img = PIL.Image.new('RGBA', (self.x,self.y), 0)
            img = PIL.Image.open(input_file)
            img = img.convert("RGBA")

        self.png_obj = img.load()

    def createpng(self):
        '''creates a png with specified holes'''

        self.__initcircles()
        self.__initalphamask()
        return self.__drawcircles()


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

        circleRadius = self.r
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
        pixdata = self.png_obj.pixdata
        for y in range(self.y):
            for x in range(self.x):
                if self.positive:
                    pixdata[x, y] = \
                        (pixdata[x,y][0],pixdata[x,y][1], pixdata[x,y][2], 255)
                else:
                    pixdata[x, y] = \
                        (pixdata[x,y][0],pixdata[x,y][1], pixdata[x,y][2], 0)
        self.png_obj.pixdata = pixdata

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

        pxDat = self.png_obj.pixdata
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
        self.png_obj.pixdata = pxDat

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
