#!/usr/bin/python
from tkinter import *
from tkinter import filedialog
from PIL import ImageTk, Image
from png_interface import png_maker
from containers import image_vars
import pint

class gui_object:
    def __init__(self):
        # All other 'global variabels' are initialized in the constructor.
        self.root = Tk()
        self.root.wm_title("Dot Maker")
        ###setup variables as tk var, set value
        #test
        self.ureg = pint.UnitRegistry()

        self.width = StringVar()
        self.width.set("2.0")

        self.height = StringVar()
        self.height.set("2.0")

        self.is_positive = BooleanVar()
        self.is_positive.set(True)

        self.dots_per_u = IntVar()
        self.dots_per_u.set('1000')

        self.dots_per_unit = StringVar()
        self.dots_per_unit.set('cm')

        self.radius = StringVar()
        self.radius.set('0.07')

        self.separation = StringVar()
        self.separation.set('0.2')

        self.from_Base_File = BooleanVar()
        self.from_Base_File.set(True)

        self.resep_new_units = StringVar()
        self.resep_new_units.set('mm')

        self.resep_old_units = StringVar()
        self.resep_old_units.set('mm')

        self.dimunits = StringVar()
        self.dimunits.set('cm')

        self.inpath  = StringVar()
        self.outpath = StringVar()
        self.options = Frame(self.root, borderwidth=5)
        self.options.grid(row=1, column=4)

        self.dimensionframe = Frame(self.options, borderwidth=5)
        self.dimensionframe.grid(row=6, columnspan=4)
        self.canvass1 = Canvas(self.root, width=240, height=240, bg='gray')
        self.canvass2 = Canvas(self.root, width=240, height=240, bg='gray')
        self.__create_GUI()

    def __unit_update(self, dummy):
        """update radius and separation values based on the chosen unit"""
        self.radius.set(str(self.ureg(self.radius.get() + \
        self.resep_old_units.get()).to(self.resep_new_units.get()).magnitude))

        self.separation.set(str(self.ureg(self.separation.get()+ \
        self.resep_old_units.get()).to(self.resep_new_units.get()).magnitude))

        self.resep_old_units.set(self.resep_new_units.get())

    def __generate_image(self):
        """method that does everything needed to actually create the png"""

        # make sure all the var.set methods are returing the actual pixel values.
        # remember, var should only be given dimensions in pixels
        px_cm      = self.ureg(str(self.dots_per_u.get()) + \
                     self.dots_per_unit.get()).to("cm").magnitude
        pos        = self.is_positive.get()

        height     = self.ureg(str(self.height.get())   + \
                     self.dots_per_unit.get()).to("cm").magnitude

        width      = self.ureg(str(self.width.get())     + \
                     self.dots_per_unit.get()).to("cm").magnitude

        radius     = self.ureg(str(self.radius.get())    + \
                     self.resep_old_units.get()).to("cm").magnitude

        separation = self.ureg(str(self.separation.get()) + \
                     self.resep_old_units.get()).to("cm").magnitude

        var_container = image_vars()
        var_container.set_height(       int(float(height*px_cm)))
        var_container.set_width(        int(float(width*px_cm)))
        var_container.set_separation(   int(float(separation*px_cm)))
        var_container.set_radius(       int(float(radius*px_cm)))
        var_container.set_positive(pos)

        if self.from_Base_File:
            var_container.set_image_file(None)
        else:
            var_container.set_image_file(self.inpath)

        imageGenerator = png_maker(var_container)
        pngObject = imageGenerator.createpng()
        self.__draw_canvas(pngObject)
        ######################################
        ### pngOBJ is a PNG OBJ!!!!     ######
        ######################################
        ### put it into the canvas!     ######
        ######################################
        # Generates user prompt for input file directory
    def __browsein(self):
        """get file location string, display string, open image, make
        make resized image, display both, save both for future ref"""
        I = str(filedialog.askopenfilename())
        self.inpath.set(I)
        im2 = Image.open(I)
        self.__draw_canvas(im2)


    def __draw_canvas(self, png):
        """puts thumbnail in canvas1(left) canvas, cropped image in canvas2(left)"""
        im1 = png.resize((240,240), Image.ANTIALIAS)

        px_cm      = self.ureg(str(self.dots_per_u.get()) + \
                     self.dots_per_unit.get()).to("cm").magnitude
        separation = self.ureg(str(self.separation.get()) + \
                     self.resep_old_units.get()).to("cm").magnitude
        cropped_dim = 2*int(float(separation)*float(px_cm))
        self.canvass1.image = ImageTk.PhotoImage(im1)
        self.canvass2.image = ImageTk.PhotoImage(png)
        self.canvass1.create_image((120,120), image=self.canvass1.image)
        self.canvass2.create_image(120,120, image=self.canvass2.image)

# Generates user prompt for output file directory
    def __browseout(self):
        """get output file directory AND name, display both"""
        O = filedialog.asksaveasfilename()
        self.outpath.set(O)

# Creates the GUI we all know and love
    def __create_GUI(self):
        """organizer method for setting up GUI"""
        self.__create_labels()
        self.__create_buttons()
        self.__create_graphic()
        self.root.mainloop()

    def __create_graphic(self):
        """graphics creation method"""
        # Hm, seems like we need to self-reference a dummy eye image in our
        # resources folder. right now it's relative to your computer's filesystem
        self.canvass1.grid(row=1,column=0,columnspan=2, padx=(10,5))
        self.canvass2.grid(row=1,column=2,columnspan=2, padx=(5,10))


    def __create_buttons(self):
        """button creation method"""
        Radiobutton(self.options, text='From base file', variable = self.from_Base_File, value=1).grid(row=2, sticky='w', columnspan=4)
        Radiobutton(self.options, text='Generated', variable = self.from_Base_File, value=2).grid(row=3, sticky='w', columnspan=4)
        b = Button(self.root, text=" Browse ", command=self.__browsein)
        b.grid(row=3, column=3,sticky='e', padx=20)
        b1 = Button(self.root, text=" Browse ", command=self.__browseout)
        b1.grid(row=4, column=3, sticky='e', padx=20)
        Button(self.root, text="Generate", anchor='n',command = self.__generate_image).grid(row=3, column=4, rowspan=2, columnspan=4)
        Radiobutton(self.options, text="Positive Print", variable=self.is_positive, value=True, font=("Helvetica", 12)).grid(row=7, columnspan=2, sticky='w')
        Radiobutton(self.options, text="Negative Print", variable=self.is_positive, value=False, font=("Helvetica", 12)).grid(row=7, column=2, columnspan=2, sticky='w')

    def __create_labels(self):
        """label creation method"""
        #Main Labels
        Label(self.root, text="Dot Maker", font=("Helvetica", 18)).grid(row=0, columnspan=4)
        Label(self.options, text="  Image Created", font=("Helvetica", 14)).grid(sticky='w', columnspan=4)
        Label(self.options, text="", font=("Helvetica", 6)).grid(row=1)
        #Sub Labels
        Label(self.options, text="", font=("Helvetica", 8)).grid(row=4)
        Label(self.options, text="Options", font=("Helvetica", 14)).grid(row=5, columnspan=4, pady=(0,10))
        Label(self.dimensionframe, text="Dimensions in", font=("Helvetica", 12)).grid(row=0,sticky='e', columnspan=2)
        OptionMenu(self.dimensionframe, self.dimunits, *[chr(956)+'m','mm','cm','in'], command=None).grid(row=0, column=2,columnspan=2)
        Label(self.dimensionframe, text="w:", font=("Helvetica", 12)).grid(row=1, column=0, sticky='w')
        Entry(self.dimensionframe, font=("Helvetica", 11), width=5, \
        textvariable=self.height).grid(row=1, column=1, sticky='w')
        Label(self.dimensionframe, text=" h:", font=("Helvetica", 12)).grid(row=1, column=2, sticky='w')
        Entry(self.dimensionframe, font=("Helvetica", 11), width=5, \
        textvariable=self.width).grid(row=1, column=3, sticky='w')
        Label(self.options, text="   Dot Density:",font=("Helvetica", 11)).grid(row=8, sticky='w')
        Label(self.options, text="   Dot Separation:",font=("Helvetica", 11)).grid(row=9, sticky='w')
        Label(self.options, text="   Dot Radius:",font=("Helvetica", 11)).grid(row=10, sticky='w')
        Entry(self.options, font=("Helvetica", 11),width=5, \
        textvariable=self.dots_per_u).grid(row=8,column=2,columnspan=2, sticky='w')
        Label(self.options, text="px per",font=("Helvetica", 11)).grid(row=8,column=3, sticky='w')
        OptionMenu(self.options, self.dots_per_unit, *[chr(956)+'m','mm','cm','in']).grid(row=8, column=4, sticky='w')
        Entry(self.options, font=("Helvetica", 11), width=5, \
        textvariable=self.separation).grid(row=9, column=2,sticky='w')
        OptionMenu(self.options, self.resep_new_units, *[chr(956)+'m','mm','cm','in'], command=self.__unit_update).grid(row=9, column=3,rowspan=2)
        Entry(self.options, font=("Helvetica", 11), width=5, \
        textvariable=self.radius).grid(row=10,column=2, columnspan=2,sticky='w')

        Label(self.root, text="Input File Path:").grid(row=3, column=0, sticky='W')
        Label(self.root, text="Output File Path:").grid(row=4, column=0, sticky='W')
        Label(self.root, textvariable=self.inpath, width=30, anchor='e', justify='right').grid(row=3, column=1, sticky='e', columnspan=2)
        Label(self.root, textvariable=self.outpath, width=30, anchor='e', justify='right').grid(row=4, column=1, columnspan=2)
