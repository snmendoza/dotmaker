#!/usr/bin/python
from tkinter import *
from tkinter import filedialog

class gui_object:
    def __init__(self):
# All other 'global variabels' are initialized in the constructor.
        self.root = Tk()
        self.from_Base_File = IntVar()
        self.inpath  = StringVar()
        self.outpath = StringVar()
        self.__create_GUI()
        self.options=Frame(self.root).grid(row=1, column=4)

# I'm assuming this is to pull in files from a directory
    def __browsein(self):
        I = filedialog.askdirectory(parent=self.root, initialdir='~/')
        self.inpath.set(I)

# I'm assuming this is to save files in a directory
    def __browseout(self):
        O = filedialog.askdirectory(parent=self.root, initialdir='~/')
        self.outpath.set(O)

# Creates the GUI we all know and love
    def __create_GUI(self):
        self.__create_labels()
        self.__create_buttons()
        self.__create_graphic()

        #what do these two do vvv ??
        self.root.after(10, root.update_idletasks())
        self.root.mainloop()

    def __create_graphic(self):
        # Hm, seems like we need to self-reference a dummy eye image in our
        # resources folder. right now it's relative to your computer's filesystem
        image = PhotoImage(file="/Users/sean/Documents/Contact GUI/dot.gif")
        dotimage = Label(root, image=image, height=210, width=240)
        dotimage.image = image
        dotimage.grid(row=1,column=0,columnspan=2, padx=(10,5))
        image2 = PhotoImage(file="/Users/sean/Documents/Contact GUI/dot.gif")
        dotimage2 = Label(root, image=image, height=210, width=240)
        dotimage2.image = image
        dotimage2.grid(row=1,column=2,columnspan=2, padx=(5,10))

    def __create_buttons(self):
        Radiobutton(self.options, text='From base file', variable = self.from_Base_File, value=1).grid(row=2, sticky='w')
        Radiobutton(self.options, text='Generated', variable = self.from_Base_File, value=2).grid(row=3, sticky='w')
        b = Button(self.root, text=" Browse ", command=self.__browsein())
        b.grid(row=3, column=3,sticky='e', padx=20)
        b1 = Button(self.root, text=" Browse ", command=self.__browseout())
        b1.grid(row=4, column=3, sticky='e', padx=20)
        Button(self.root, text=" Generate ", padx=5, pady=5).grid(row=3, column=4, rowspan=2)

    def __create_labels(self):
        #Main Labels
        Label(self.root, text="Dot Maker", font=("Helvetica", 18)).grid(row=0, columnspan=4)
        Label(self.options, text="  Image Created", font=("Helvetica", 14)).grid(sticky='w')
        Label(self.options, text="", font=("Helvetica", 6)).grid(row=1)
        #Sub Labels
        Label(self.options, text="", font=("Helvetica", 8)).grid(row=4)
        Label(self.options, text="  Options", font=("Helvetica", 14)).grid(row=5, sticky='w')
        Label(self.root, text="Input File Path:").grid(row=3, column=0, sticky='W')
        Label(self.root, text="Output File Path:").grid(row=4, column=0, sticky='W')
        Label(self.root, textvariable=self.inpath).grid(row=3, column=1, sticky='W')
        Label(self.root, textvariable=self.outpath).grid(row=4, column=1, sticky='W')
