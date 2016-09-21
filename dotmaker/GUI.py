#!/usr/bin/python
from tkinter import *
from tkinter import filedialog
from PIL import ImageTk, Image

class gui_object:
    def __init__(self, var):
# All other 'global variabels' are initialized in the constructor.
        self.root = Tk()


        ###setup variables as tk var, set value
        self.var = var
        self.var.width = IntVar()
        self.var.width.set(100)
        self.var.height = IntVar()
        self.var.height.set(100)
        self.var.is_positive = BooleanVar()
        self.var.is_positive.set(True)
        self.var.dots_per_cm = IntVar()
        self.var.dots_per_cm.set(1000)
        self.var.separation = IntVar()
        self.var.separation.set(200)
        self.var.radius = IntVar()
        self.var.radius.set(70)
        self.var.image_file = None
        self.var.width = IntVar()
        self.var.width.set(100)
        ###

        self.from_Base_File = BooleanVar()
        self.from_Base_File.set(True)
        self.inpath  = StringVar()
        self.outpath = StringVar()
        self.options = Frame(self.root, borderwidth=5)
        self.options.grid(row=1, column=4)
        self.canvass1 = Canvas(self.root, width=240, height=240, bg='gray')
        self.canvass2 = Canvas(self.root, width=240, height=240, bg='gray')
        self.__create_GUI()


# Generates user prompt for input file directory
    def __browsein(self):
        """get file location string, display string, open image, make
        make resized image, display both, save both for future ref"""
        I = str(filedialog.askopenfilename())
        self.inpath.set(I)
        im2 = Image.open(I)
        im1 = im2.resize((240,240), Image.ANTIALIAS)
        self.canvass1.image = ImageTk.PhotoImage(im1)
        self.canvass2.image = ImageTk.PhotoImage(im2)
        self.canvass1.create_image((120,120), image=self.canvass1.image)
        self.canvass2.create_image(120,120, image=self.canvass2.image)

# Generates user prompt for output file directory
    def __browseout(self):
        """get output file directory AND name, display both"""
        O = filedialog.asksaveasfilename()
        self.outpath.set(O)

# Creates the GUI we all know and love
    def __create_GUI(self):
        self.__create_labels()
        self.__create_buttons()
        self.__create_graphic()
        self.root.mainloop()

    def __create_graphic(self):
        # Hm, seems like we need to self-reference a dummy eye image in our
        # resources folder. right now it's relative to your computer's filesystem
        self.canvass1.grid(row=1,column=0,columnspan=2, padx=(10,5))
        self.canvass2.grid(row=1,column=2,columnspan=2, padx=(5,10))


    def __create_buttons(self):
        Radiobutton(self.options, text='From base file', variable = self.from_Base_File, value=1).grid(row=2, sticky='w', columnspan=4)
        Radiobutton(self.options, text='Generated', variable = self.from_Base_File, value=2).grid(row=3, sticky='w', columnspan=4)
        b = Button(self.root, text=" Browse ", command=self.__browsein)
        b.grid(row=3, column=3,sticky='e', padx=20)
        b1 = Button(self.root, text=" Browse ", command=self.__browseout)
        b1.grid(row=4, column=3, sticky='e', padx=20)
        Button(self.root, text="Generate", anchor='n').grid(row=3, column=4, rowspan=2, columnspan=4)
        Radiobutton(self.options, text="Positive Print", variable=self.var.is_positive, value=True, font=("Helvetica", 12)).grid(row=7, columnspan=2, sticky='w')
        Radiobutton(self.options, text="Negative Print", variable=self.var.is_positive, value=False, font=("Helvetica", 12)).grid(row=7, column=2, columnspan=2, sticky='w')

    def __create_labels(self):
        #Main Labels
        Label(self.root, text="Dot Maker", font=("Helvetica", 18)).grid(row=0, columnspan=4)
        Label(self.options, text="  Image Created", font=("Helvetica", 14)).grid(sticky='w', columnspan=4)
        Label(self.options, text="", font=("Helvetica", 6)).grid(row=1)
        #Sub Labels
        Label(self.options, text="", font=("Helvetica", 8)).grid(row=4)
        Label(self.options, text="Options", font=("Helvetica", 14)).grid(row=5, columnspan=4, pady=(0,10))
        Label(self.options, text="  Dimensions:", font=("Helvetica", 12)).grid(row=6, sticky='w', columnspan=2)
        Entry(self.options, font=("Helvetica", 11), width=5, textvariable=self.var.width).grid(row=6, column=2, sticky='w')
        Entry(self.options, font=("Helvetica", 11), width=5,textvariable=self.var.height).grid(row=6, column=3, sticky='w')
        Label(self.options, text="   DPI:",font=("Helvetica", 11)).grid(row=8, sticky='w')
        Label(self.options, text="   Dot Separation:",font=("Helvetica", 11)).grid(row=9, sticky='w')
        Label(self.options, text="   Dot Radius:",font=("Helvetica", 11)).grid(row=10, sticky='w')
        Entry(self.options, font=("Helvetica", 11),width=14, textvariable=self.var.dots_per_cm).grid(row=8,column=2,columnspan=2, sticky='w')
        Entry(self.options, font=("Helvetica", 11), width=14, textvariable=self.var.separation).grid(row=9, column=2,columnspan=2,sticky='w')
        Entry(self.options, font=("Helvetica", 11), width=14, textvariable=self.var.radius).grid(row=10,column=2, columnspan=2,sticky='w')

        Label(self.root, text="Input File Path:").grid(row=3, column=0, sticky='W')
        Label(self.root, text="Output File Path:").grid(row=4, column=0, sticky='W')
        Label(self.root, textvariable=self.inpath, width=30, anchor='e', justify='right').grid(row=3, column=1, sticky='e', columnspan=2)
        Label(self.root, textvariable=self.outpath, width=30, anchor='e', justify='right').grid(row=4, column=1, columnspan=2)
