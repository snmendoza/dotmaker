#!/usr/bin/python
from tkinter import *
from tkinter import filedialog


def browsein():
    I = filedialog.askdirectory(parent=root, initialdir='~/')
    inpath.set(I)
def browseout():
    O = filedialog.askdirectory(parent=root, initialdir='~/')
    outpath.set(O)

root = Tk()
var = IntVar()
inpath  = StringVar()
outpath = StringVar()



Label(root, text="Dot Maker", font=("Helvetica", 18)).grid(row=0, columnspan=4)

options=Frame(root)
options.grid(row=1, column=4)
Label(options, text="  Image Created", font=("Helvetica", 14)).grid(sticky='w')
Label(options, text="", font=("Helvetica", 6)).grid(row=1)
Radiobutton(options, text='From base file', variable = var, value=1).grid(row=2, sticky='w')
Radiobutton(options, text='Generated', variable = var, value=2).grid(row=3, sticky='w')
Label(options, text="", font=("Helvetica", 8)).grid(row=4)
Label(options, text="  Options", font=("Helvetica", 14)).grid(row=5, sticky='w')

image = PhotoImage(file="/Users/sean/Documents/Contact GUI/dot.gif")
dotimage = Label(root, image=image, height=210, width=240)
dotimage.image = image
dotimage.grid(row=1,column=0,columnspan=2, padx=(10,5))

image2 = PhotoImage(file="/Users/sean/Documents/Contact GUI/dot.gif")
dotimage2 = Label(root, image=image, height=210, width=240)
dotimage2.image = image
dotimage2.grid(row=1,column=2,columnspan=2, padx=(5,10))

Label(root, text="Input File Path:").grid(row=3, column=0, sticky='W')
Label(root, text="Output File Path:").grid(row=4, column=0, sticky='W')

Label(root, textvariable=inpath).grid(row=3, column=1, sticky='W')
Label(root, textvariable=outpath).grid(row=4, column=1, sticky='W')

b = Button(root, text=" Browse ", command=browsein)
b.grid(row=3, column=3,sticky='e', padx=20)
b1 = Button(root, text=" Browse ", command=browseout)
b1.grid(row=4, column=3, sticky='e', padx=20)
Button(root, text=" Generate ", padx=5, pady=5).grid(row=3, column=4, rowspan=2)

root.after(10, root.update_idletasks())
root.mainloop()
