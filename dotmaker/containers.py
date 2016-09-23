from tkinter import *
import sys
import os.path

class image_vars:
    def __init__(self):

        self.conversionFactor = 1
        self.is_positive=True
        self.dots_per_cm=1000
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

    #sets the desired dimensions in cm units
    def set_dimensions(self,dim):
        self.dimensions = dim

    #sets whether a print is positive or negative
    def set_positive(self,pos):
        self.is_positive = pos

    #sets cm to dots capability of the printer
    def set_dots_per_cm(self,dpcm):
        self.dots_per_cm = dpcm

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
    def get_width_pixels(self):
        return self.dimensions[0]*(self.dots_per_cm)

    #gets the print height in pixels
    def get_height_pixels(self):
        return self.dimensions[1]*(self.dots_per_cm)

    #returns whether the print should be positive or not
    def get_positive(self):
        return self.is_positive

    #gets the cirlce/dot separation in px
    def get_dot_px_separation(self):
        return self.separation*(self.dots_per_cm)

    #gets the cirlce/dot radius in px
    def get_dot_px_radius(self):
        return self.radius*(self.dots_per_cm)
