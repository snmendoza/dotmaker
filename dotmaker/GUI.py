#!/usr/bin/python
from tkinter import *
from tkinter import filedialog
from PIL import ImageTk, Image
from png_interface import png_maker
import pint

class gui_object:
	def __init__(self, var):
		# All other 'global variabels' are initialized in the constructor.
		self.root = Tk()

		###setup variables as tk var, set value
		self.var = var
		self.ureg = pint.UnitRegistry()

		### The following variables are all the control variables, set up for
		# binding with tkinter/GUI object. It may be possible to directly
		# bind these to var containers vars, but that method is still
		# unkown to me
		###
		self.from_Base_File = BooleanVar()
		self.from_Base_File.set(True)
		self.x = StringVar()
		self.x.set('100')
		self.y = StringVar()
		self.y.set('100')
		self.positive = BooleanVar()
		self.positive.set(False)
		self.dots_per_cm = StringVar()
		self.dots_per_cm.set('500')
		self.radius = StringVar()
		self.radius.set('2')
		self.separation = StringVar()
		self.separation.set('5')
		self.resep_new_units = StringVar()
		self.resep_new_units.set('mm')
		self.resep_old_units = StringVar()
		self.resep_old_units.set('mm')



		self.inpath  = StringVar()
		self.outpath = StringVar()
		self.options = Frame(self.root, borderwidth=5)
		self.options.grid(row=1, column=4)
		self.canvass1 = Canvas(self.root, width=240, height=240, bg='gray')
		self.canvass2 = Canvas(self.root, width=240, height=240, bg='gray')
		self.__create_GUI()

	def _unit_update(self, dummy):
		"""update radius and separation values based on the chosen units"""
		self.radius.set(str(self.ureg(self.radius.get()+self.resep_old_units.get()).to(self.resep_new_units.get()).magnitude))
		self.separation.set(str(self.ureg(self.separation.get()+self.resep_old_units.get()).to(self.resep_new_units.get()).magnitude))
		self.resep_old_units.set(self.resep_new_units.get())

	def __generate_image(self):
		"""Takes all tkinter GUI variables, converts to px where appropriate
		sets all var container vars accordingly

		Calls png maker, generates file and displays to GUI"""

		self.var.set_dimensions([int(self.x.get()), int(self.y.get())])
		self.var.set_radius(int(float(self.ureg(self.radius.get()+self.resep_old_units.get()).to('cm').magnitude)*int(self.dots_per_cm.get())))
		self.var.set_separation(int(float(self.ureg(self.separation.get()+self.resep_old_units.get()).to('cm').magnitude)*int(self.dots_per_cm.get())))
		self.var.set_positive(self.positive.get())
		self.var.set_dots_per_cm(int(self.dots_per_cm.get()))
		imageGenerator = png_maker(self.var)
		pngObject = imageGenerator.createpng()
		draw_canvas(pngObject)
		######################################
		### pngOBJ is a PNG OBJ!!!!	 ######
		######################################
		### put it into the canvas!	 ######
		######################################
# Generates user prompt for input file directory
	def __browsein(self):
		"""get file location string, display string, open image, make
		make resized image, display both, save both for future ref"""
		I = str(filedialog.askopenfilename())
		self.inpath.set(I)
		im2 = Image.open(I)
		self._draw_canvas(im2)


	def _draw_canvas(self, png):
		"""puts thumbnail in canvas1(left) canvas, cropped image in canvas2(left)"""
		im1 = png.resize((240,240), Image.ANTIALIAS)
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
		Button(self.root, text="Generate", anchor='n',command = self.__generate_image).grid(row=3, column=4, rowspan=2, columnspan=4)
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
		Entry(self.options, font=("Helvetica", 11), width=5, \
		textvariable=self.x).grid(row=6, column=2, sticky='w')
		Entry(self.options, font=("Helvetica", 11), width=5, \
		textvariable=self.y).grid(row=6, column=3, sticky='w')
		Label(self.options, text="   Dot Density:",font=("Helvetica", 11)).grid(row=8, sticky='w')
		Label(self.options, text="   Dot Separation:",font=("Helvetica", 11)).grid(row=9, sticky='w')
		Label(self.options, text="   Dot Radius:",font=("Helvetica", 11)).grid(row=10, sticky='w')
		Entry(self.options, font=("Helvetica", 11),width=5, \
		textvariable=self.dots_per_cm).grid(row=8,column=2,columnspan=2, sticky='w')
		Entry(self.options, font=("Helvetica", 11), width=5, \
		textvariable=self.separation).grid(row=9, column=2,sticky='w')
		OptionMenu(self.options, self.resep_new_units, *[chr(956)+'m','mm','cm','in'], command=self._unit_update).grid(row=9, column=3,rowspan=2)
		Entry(self.options, font=("Helvetica", 11), width=5, \
		textvariable=self.radius).grid(row=10,column=2, columnspan=2,sticky='w')

		Label(self.root, text="Input File Path:").grid(row=3, column=0, sticky='W')
		Label(self.root, text="Output File Path:").grid(row=4, column=0, sticky='W')
		Label(self.root, textvariable=self.inpath, width=30, anchor='e', justify='right').grid(row=3, column=1, sticky='e', columnspan=2)
		Label(self.root, textvariable=self.outpath, width=30, anchor='e', justify='right').grid(row=4, column=1, columnspan=2)
