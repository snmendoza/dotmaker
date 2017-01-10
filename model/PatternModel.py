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
        self.__analyze_pattern()

    def __defineVars(self,vardict):
        self.r  = vardict.get("radius")
        self.p  = vardict.get("is_positive")
        self.s  = round(vardict.get("separation"),0)
        self.s_12 = int(round(self.s*math.sqrt(1/2),0))
        self.cellSize = (self.s_12*2+1,self.s_12*2+1)
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
        s = self.s_12
        radius = (-r,-r, r, r)
        draw = ImageDraw.Draw(self.mask)
        for x in range(0,2):
            for y in range(0,2):
                b = (s*x*2,s*y*2,s*x*2,s*y*2)
                draw.ellipse(tuple(map(operator.add, radius, b)),fill=self.circle)

        b = (s,s,s,s)
        draw.ellipse(tuple(map(operator.add, radius, b)),fill=self.circle)
        del draw

    def __analyze_pattern(self):

        self.numericalOpacity   = get_numerical_opacity(self)
        self.theoreticalOpacity = get_theoretical_opacity(self)

    def get_mask(self):
        return self.mask.copy()

    def getImage(self):
        temp = PIL.Image.new('RGBA',self.cellSize,0)
        return PIL.Image.alpha_composite(temp, self.mask)

def get_theoretical_opacity(cell):
    r = float(cell.r)
    s = float(cell.s)
    s2 = s*s
    r2 = r*r
    if 2*r < s:
        print("smaller")
        positive_opacity = math.pi*r2 / s2
    else:
        print("very big")
        segment_degrees   = 2*math.acos(s/(2*r))
        segment_area      = r2*(segment_degrees - math.sin(segment_degrees)) / 2
        positive_opacity = (math.pi*r2 / 2 -2 * segment_area) / (s2 / 2)
        print("segment_Area:" + str(segment_area))

    if cell.p:
        return positive_opacity
    else:
        return 1-positive_opacity


def get_numerical_opacity(cell):
    temp_img = cell.getImage()
    width, height = temp_img.size
    alpha_sum     = 0
    for x in range(0,width):
        for y in range(0,height):
            pixel_tuple = temp_img.getpixel((x,y))
            alpha_sum = alpha_sum + pixel_tuple[3]

    return alpha_sum / (255*width*height)

def __getPreImage(varDict):
    size = (varDict.get("width"), varDict.get("height"))
    if varDict.get("input_file") == None:
        img = PIL.Image.new('RGBA', size, (0,0,0,255))
    else:
        img = varDict["input_file"].copy()
        img = img.convert("RGBA")
        img = img.resize(size)
    return img

def createMultiPrintCell(cellDicts):
    ## need a dummy image, mask, and
    size = (200, 200)
    t=[]
    n=[]
    m = PIL.Image.new('RGBA', size ,255)
    for left in range(0, 2):
        for top in range(0, 2):
            cell = UnitCell(cellDicts[left][top])
            img = cell.getImage()
            t.append(cell.theoreticalOpacity)
            n.append(cell.numericalOpacity)
            img = img.resize((100,100))
            m.paste(img, (left*100, top*100),mask=img)

    return (m,t,n)

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

def createMultiPrintPng(document,printdicts):
    ## need a dummy image, mask, and
    docSize = (document['documentWidth'], document['documentHeight'])
    pResize = (document['printWidth'], document['printHeight'])
    margin  = document['printMargin']
    xlength = len(printdicts)
    ylength = len(printdicts[0])
    main = PIL.Image.new('RGBA', docSize, 0)
    for x in range(xlength):
        for y in range(ylength):
            img = createSinglePrintPng(printdicts[x][y])
            img = img.resize((pResize[0],pResize[1]))
            main.paste(img, (margin+x*(pResize[0] + margin), margin+y*(pResize[1] + margin)),mask=img)

    return main
