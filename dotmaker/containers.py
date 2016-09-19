
import sys
import os.path

class image_vars:
    def __init__(self):
        self.dimensions = (100,100)
        self.is_positive = True
        self.dots_per_cm = 1000
        self.separation = 200
        self.radius = 70
        self.image_file = None

    def set_image_file(self,imgFile):
        if imgFile is None:
            self.image_file = None
        else:
            if os.path.isfile(imgFile):
                if os.access(imgFile, os.R_OK):
                    if imghdr.what(imgFile)=='png':
                        self.image_file=imgFile
                    else:
                        print("* Looks like input file is type " +imghdr.what(self.pngFilePath))
                        print("* Please use input image of type png!!!")
                else:
                    print("* Warning!!! File does not have access permissions")
            else:
                print("* File seems to be missing!!! Maybe path is incorrect?")

    def set_dimensions(self,dim):
        self.dimensions = dim

    def set_positive(self,pos):
        self.is_positive = pos

    def set_dots_per_cm(self,dpcm):
        self.dots_per_cm = dpcm

    def set_separation(self,sep):
        self.separation = sep

    def set_radius(self,rad):
        self.radius = rad

    def get_image_file(self):
        return self.image_file

    def get_dimensions(self):
        return self.dimensions

    def get_positive(self):
        return self.is_positive

    def get_dots_per_cm(self):
        return self.dots_per_cm

    def get_dot_separation(self):
        return self.separation

    def get_dot_radius(self):
        return self.radius
