import sys
import os.path
import imghdr
import PIL.Image
import math
from copy import deepcopy

class png_maker:
    def __init__(self, option):
        ''' inits the png_maker object with options. Options range from 1-3
        and correspond to different image file creation pathways'''
        self.pngFilePath=""
        self.validFile=False
        self.validPath=False
        self.circles = []
        self.option = option
        if option     ==1:
            self.__menu_1()
        elif option   ==2:
            self.__menu_2()
        elif option   ==3:
            self.__menu_3()

    def __menu_1(self):
        '''creates image via an input file'''
        print("""\n
*********************************************************
* To have Dot Maker edit a png image, you must first    *
* input the file path                                   *
*********************************************************\n""")

        self.pngFilePath = input("")
        self.__checkFile()

    def __menu_2(self):
        '''creates a blank image, but uses the provided path to save'''
        print("""\n
*********************************************************
* To have Dot Maker make a png image, you must first    *
* input the folder path                                 *
*********************************************************\n""")
        self.pngFilePath = input("")
        self.__checkPath()

    def __menu_3(self):
        '''currently unimplemented'''
        print("""\n
*********************************************************
* To have Dot Maker make a series of png images, you    *
* must first input the folder path                      *
*********************************************************\n""")
        self.pngFilePath = input("")
        self.__checkPath()

    def __checkFile(self):
        '''ensures the file is a openable, uncorrupted png'''
        print("\n*********************************************************")
        if os.path.isfile(self.pngFilePath):
            print("* File exists")
            if os.access(self.pngFilePath, os.R_OK):
                print("* File has correct permissions")

                # Next line can allow bad data through if fed a png data file with no data, see
                # mt1.png for an example of this
                if imghdr.what(self.pngFilePath)=='png':
                    print("* Input file is a png")
                    self.validFile=True
                else:
                    # Next line can crash if given garbage data, see test2.what for an example of this
                    # In general, if given non-image data, it may crash. For example, giving it 'main.py'
                    # at this point causes a crash.
                    print("* Looks like input file is type " +imghdr.what(self.pngFilePath))
                    print("* Please use input image of type png!!!")
            else:
                print("* Warning!!! File does not have access permissions")
        else:
            print("* File seems to be missing!!! Maybe path is incorrect?")
        print("*********************************************************\n")

    def __checkPath(self):
        '''ensures the folder is a folder and is accessible'''
        print("\n*********************************************************")
        if os.path.isdir(self.pngFilePath):
            print("File exists")
            if os.access(self.pngFilePath, os.R_OK):
                self.validPath=True
                print("File has correct permissions")
            else:
                print("Directory cannot be accessed!!!")
        else:
            print("Path is not valid directory!!!")
        print("*********************************************************\n")

    def __params(self):
        '''gets all the needed image parameters from the user'''
        print("\n*********************************************************")
        print("\n* Is print a negative (transparent dots)(y/n)?")
        self.isNeg = input("")
        print("\n* Enter radius of dots in µm")
        dotsize = int(input(""))
        print("\n* Enter spacing of dots in µm")
        dotspacing = int(input(""))
        print("\n* Enter the pixels per cm of your printer")
        self.px_cm = int(input(""))
        if self.option !=1:
            print("\n* Enter width/height of your .png in cm")
            cm = int(input(""))
            self.cm = cm
            print("*********************************************************\n")
        self.dotsize = int(self.px_cm*dotsize*0.0001) #µm to px conversion
        self.dotspacing = int(self.px_cm*dotspacing*0.0001) #µm to px conversion

    def multipng(self):
        print("\n* Is print a negative (transparent dots)(y/n)?")
        self.isNeg = input("")
        print("""\n
*********************************************************
* Enter the side length in cm of the png files          *
* you wish to generate                                  *
*********************************************************\n""")
        self.cm = int(input(""))
        print("""\n
*********************************************************
* Enter the pixels per cm of your printer               *
*********************************************************\n""")
        self.px_cm = int(input(""))
        print("""\n
*********************************************************
* Enter the starting circle radius, ending radius, and  *
* number of intervals between in (µm,µm,#)              *
*********************************************************\n""")
        radinfo = input("")
        print("""
*********************************************************
* Enter the starting circle separation, ending          *
* separation, and number of intervals between in        *
* (µm,µm,#)                                             *
*********************************************************\n""")
        sepinfo = input("")

        sepinfo = sepinfo.replace(")","")
        sepinfo = sepinfo.replace("(","")
        radinfo = radinfo.replace(")","")
        radinfo = radinfo.replace("(","")
        radinfo = radinfo.split(",")
        sepinfo = sepinfo.split(",")

        beginning_radius    = int(radinfo[0])
        ending_radius       = int(radinfo[1])
        if beginning_radius > ending_radius:
            radius_interval = beginning_radius - ending_radius
        else:
            radius_interval = ending_radius - beginning_radius
        radius_interval     = int(radius_interval/int(radinfo[2]))

        beginning_sep       = int(sepinfo[0])
        ending_sep          = int(sepinfo[1])
        if beginning_sep    > ending_sep:
            sep_interval    = beginning_sep - ending_sep
        else:
            sep_interval    = ending_sep - beginning_sep
        sep_interval        = int(sep_interval/int(sepinfo[2]))

        total_iterations = int(sepinfo[2])*int(radinfo[2])


        print("""\n
*********************************************************
* Creating """ + str(total_iterations) + " png files""""
*********************************************************""")
        # Set up loop
        # create hard alpha mask copy that is hopefully immutable
        count = 0
        print(" ")
        png_obj = png_object(self)
        self.pngobj = png_obj
        pixcopy = self.pngobj.img.copy()

        for radius in range(int(radinfo[2])+1):
            self.dotsize = int(((beginning_radius\
                                + radius*radius_interval)\
                                *0.0001*(self.px_cm)))
            self.__initcircles()
            # only have to run init circles once per radius
            for separation in range(int(sepinfo[2])+1):
                it = int(count*100 / total_iterations)
                print ("\r Completing:" + str(it) + "% ", end="")
                # then set up separation stuff.
                self.__initalphamask()
                self.dotspacing = int(((beginning_sep\
                                    + separation*sep_interval)\
                                    *0.0001*(self.px_cm)))
                # now make png.
                self.createpng(True)
                count=count+1
    def createpng(self,scan):
        '''creates a png with specified holes'''
        if not(scan):
            self.__params()
            png_obj = png_object(self)
            self.pngobj = png_obj
            print("""
\n*********************************************************
* Editing .png Alpha.                                   *
* This may take some time                               *
*********************************************************\n""")
            self.__initcircles()
            self.__initalphamask()
        self.__drawcircles()
        self.__savetofile()

    def __initalphamask(self):
        ''' Puts an alpha mask of 0 or 1 across the image,
        depending on input parameters'''
        pixdata = self.pngobj.pixdata
        if self.isNeg == "y" or self.isNeg == "Y":
            flip = True
        else:
            flip = False
        for y in range(self.pngobj.img.size[1]):
            for x in range(self.pngobj.img.size[0]):
                if flip:
                    pixdata[x, y] = \
                        (pixdata[x,y][0],pixdata[x,y][1], pixdata[x,y][2], 255)
                else:
                    pixdata[x, y] = \
                        (pixdata[x,y][0],pixdata[x,y][1], pixdata[x,y][2], 0)
        self.pngobj.pixdata = pixdata

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

        self.circles = []
        circleRadius = self.dotsize
        circleRadiusSquared = circleRadius*circleRadius
        for x in range(circleRadius):
            ybase = 0
            while (ybase*ybase + x*x) <= circleRadiusSquared:
                self.circles.append((x,ybase))
                self.circles.append((-x,ybase))
                self.circles.append((-x,-ybase))
                self.circles.append((x,-ybase))
                ybase=ybase+1

    def __drawcircles(self):
        '''places circles across the alpha layer of the png'''
        # This function raster scans across the png image
        # There are two types of scans.
        # One starts at 0,0 and iterates up x and y by iterator 2*separation/sqrt(2)
        # The second starts at separation/sqrt(2), separation/sqrt(2) and iterates
        # up x and y by 2*separation/sqrt(2)
        # The 2/root(2) comes from geometry relations between the circle centers

        # ******************* Iterator variables ******************
        sep        = self.dotspacing
        root2       = 1/(math.sqrt(2))

        x_1         = sep*root2
        x_i         = sep*root2*2
        y_1         = sep*root2
        y_i         = sep*root2*2

        xwidth      = self.pngobj.img.size[0]
        yheight     = self.pngobj.img.size[1]

        # dividing total pixel length on one side by the width of the iterator
        # gives us the expected number of iterations per raster scan.
        dimensions  = (xwidth,yheight)
        x_f         = int(xwidth/x_i)
        y_f         = int(yheight/y_i)
        # *********************************************************
        # ******************* Extraneous Loop things **************

        # tells us whether the alpha value should be zero or not
        if self.isNeg == "y" or self.isNeg == "Y":
            alpha = 0
        else:
            alpha = 255

        pxDat = self.pngobj.pixdata
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
        self.pngobj.pixdata = pxDat

    def __getAdjustedPoints(self,centerCoordinate,dimensions):
        '''Adjusts each point within the circle list
        to have a center around given coordinates'''
        # This function takes the list of circle points and offsets them via
        # the given x,y coordinate. Also passes the xwidth and y width to ensure
        # only circle pixels within the frame are passed
        c_x = centerCoordinate[0]
        c_y = centerCoordinate[1]
        newlist = []

        if  c_x  - (self.dotsize)>= 0 and self.dotsize + c_x < dimensions[0] \
        and c_y -  (self.dotsize)>=0  and self.dotsize + c_y <dimensions[1]:
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

    def __savetofile(self):

        filename = "Type__" + self.isNeg + ""\
                    "dot_size__" \
                    "" + str(int(self.dotsize*10000/(self.px_cm))) + "" \
                    "_dot_spacing__" \
                    "" + str(int(self.dotspacing*10000/(self.px_cm))) + ".png"
        if self.validFile:
            path = os.path.split(self.pngFilePath)
            path = path[0]
        else:
            path = self.pngFilePath
        path = os.path.join(path,filename)
        self.pngobj.img.save(path,"png")

class png_object:
    '''a container for the png data'''
    def __init__(self, pnginterface):
        if pnginterface.validFile:
            self.img = PIL.Image.open(pnginterface.pngFilePath)
            self.img = self.img.convert("RGBA")
            self.pixdata = self.img.load()
        else:
            self.x = pnginterface.px_cm*(pnginterface.cm)
            self.y = pnginterface.px_cm*(pnginterface.cm)
            self.img = PIL.Image.new('RGBA', (self.x,self.y), 0)
            self.pixdata = self.img.load()
