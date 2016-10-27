#!/usr/bin/python
import tkinter as tk
from PIL import ImageTk, Image
import pint

class base_generation_frame(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.__define_vars()
        self.__define_buttons()
        self.__align_buttons()

    def __define_vars(self):
        self.label_font = ("Helvetica", 11)
        self.entry_font = ("Helvetica", 11)
        self.gen_option = 1

        self.ureg = pint.UnitRegistry()

        self.inpath  = tk.StringVar()
        self.outpath = tk.StringVar()

        self.unit = tk.StringVar()
        self.unit.set('cm')

        self.temp_unit = tk.StringVar()
        self.temp_unit.set('cm')

        self.height = tk.StringVar()
        self.height.set('2')

        self.width = tk.StringVar()
        self.width.set('2')

    def __define_buttons(self):
        #labels:
        self.width_lab  = tk.Label(self, text="Image width:",font=self.label_font)
        self.height_lab = tk.Label(self, text="Image height:",font=self.label_font)
        #entry:
        self.width_ent  = tk.Entry(self, textvariable=self.width, font=self.entry_font,width=5)
        self.height_ent = tk.Entry(self, textvariable=self.height,font=self.entry_font,width=5)
        #Generation Options
        self.base_but   = tk.Radiobutton(self, text='From base file',font=self.label_font, variable = self.gen_option, value=2)
        self.gen_but    = tk.Radiobutton(self, text='Generated',font=self.label_font, variable = self.gen_option, value=1)
        #option menu:
        self.dot_menu   = tk.OptionMenu(self, self.temp_unit, \
                    *[chr(956)+'m','mm','cm','in'], command=self.__dim_update)


    def __align_buttons(self):
        self.grid_columnconfigure(0,minsize=100)
        self.grid_columnconfigure(1,minsize=100)
        self.grid_columnconfigure(2,minsize=50)

        self.grid_rowconfigure(0,minsize=50)
        self.grid_rowconfigure(1,minsize=30)
        self.grid_rowconfigure(2,minsize=30)

        self.dot_menu.grid(row=1,column=2,sticky='w')

        self.width_lab .grid(row=1,column=0,sticky='w')
        self.height_lab.grid(row=2,column=0,sticky='w')

        self.width_ent.grid(row=1,column=1,sticky='w')
        self.height_ent.grid(row=2,column=1,sticky='w')

        self.base_but.grid(row=0,column=0,sticky='w')
        self.gen_but.grid(row=0,column=2,sticky='w')


    def __dim_update(self,update):
        self.height.set(str(self.ureg(self.height.get() + \
        self.unit.get()).to(update).magnitude))

        self.width.set(str(self.ureg(self.width.get()+ \
        self.unit.get()).to(update).magnitude))

        self.unit.set(update)

        def __browsein(self):
            """get file location string, display string, open image, make
            make resized image, display both, save both for future ref"""
            I = str(filedialog.askopenfilename())
            self.inpath.set(I)
            im2 = Image.open(I)


class circle_param_frame(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.__define_vars()
        self.__define_buttons()
        self.__align_buttons()

    def __define_vars(self):
        self.label_font = ("Helvetica", 11)
        self.entry_font = ("Helvetica", 11)
        self.ureg = pint.UnitRegistry()

        self.pos = tk.BooleanVar()
        self.pos.set(True)

        self.temp_unit1 = tk.StringVar()
        self.temp_unit1.set('cm')

        self.temp_unit2 = tk.StringVar()
        self.temp_unit2.set('cm')

        self.pixels_per_unit_value = tk.StringVar()
        self.pixels_per_unit_value.set('1000')

        self.pixels_per_unit_unit = tk.StringVar()
        self.pixels_per_unit_unit.set('cm')

        self.radius = tk.StringVar()
        self.radius.set('0.07')

        self.separation = tk.StringVar()
        self.separation.set('0.2')

        self.unit = tk.StringVar()
        self.unit.set('mm')

    def __define_buttons(self):
        #labels:
        self.density_lab  = tk.Label(self, text="Dot Density:",font=self.label_font)
        self.dot_sep_lab  = tk.Label(self, text="Dot Separation:",font=self.label_font)
        self.dot_rad_lab  = tk.Label(self, text="Dot Radius:",font=self.label_font)
        #entry:
        self.density_ent  = tk.Entry(self, textvariable=self.pixels_per_unit_value,font=self.entry_font,width=5)
        self.dot_sep_ent  = tk.Entry(self, textvariable=self.separation, font=self.entry_font,width=5)
        self.dot_rad_ent  = tk.Entry(self, textvariable=self.radius,font=self.entry_font,width=5)
        #option menu:
        self.dot_menu     = tk.OptionMenu(self, self.temp_unit2, *[chr(956)+'m','mm','cm','in'], command=self.__circle_update)
        self.density_menu = tk.OptionMenu(self, self.temp_unit1, *[chr(956)+'m','mm','cm','in'], command=self.__density_update)
        #radiobuttons:
        self.pos_lab      = tk.Radiobutton(self, text="Positive Print", variable=self.pos, \
            value=True, font=self.label_font)
        self.neg_lab      = tk.Radiobutton(self, text="Negative Print", variable=self.pos, \
            value=False, font=self.label_font)

    def __align_buttons(self):
        self.grid_columnconfigure(0,minsize=100)
        self.grid_columnconfigure(1,minsize=100)
        self.grid_columnconfigure(2,minsize=50)

        self.grid_rowconfigure(0,minsize=30)
        self.grid_rowconfigure(1,minsize=30)
        self.grid_rowconfigure(2,minsize=30)
        self.grid_rowconfigure(3,minsize=30)

        self.density_lab.grid(row=0,column=0,sticky='w')
        self.dot_sep_lab.grid(row=1,column=0,sticky='w')
        self.dot_rad_lab.grid(row=2,column=0,sticky='w')

        self.density_ent.grid(row=0,column=1,sticky='w')
        self.dot_sep_ent.grid(row=1,column=1,sticky='w')
        self.dot_rad_ent.grid(row=2,column=1,sticky='w')

        self.dot_menu.grid(row=1,column=2,sticky='w')
        self.density_menu.grid(row=0,column=2,sticky='w')

        self.pos_lab.grid(row=3,column=0,sticky='w')
        self.neg_lab.grid(row=3,column=1,sticky='w')

    def __density_update(self,update):
        self.pixels_per_unit_value.set(str(self.ureg(self.pixels_per_unit_value.get() + \
        self.pixels_per_unit_unit.get()).to(update).magnitude))

        self.pixels_per_unit_unit.set(update)

    def __circle_update(self,update):
        self.radius.set(str(self.ureg(self.radius.get() + \
        self.unit.get()).to(update).magnitude))

        self.separation.set(str(self.ureg(self.separation.get()+ \
        self.unit.get()).to(update).magnitude))

        self.unit.set(update)

class canvass_master(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.__define_vars()
        self.__define_buttons()
        self.__align_buttons()

    def __define_vars(self):
        pass

    def __define_buttons(self):
        self.canvass1 = tk.Canvas(self, width=240, height=240, bg='gray')
        self.canvass2 = tk.Canvas(self, width=240, height=240, bg='gray')

    def __align_buttons(self):
        self.grid_columnconfigure(0,minsize=330,pad=10)
        self.grid_columnconfigure(1,minsize=330,pad=10)

        self.grid_rowconfigure(0,minsize=330,pad=10)

        self.canvass1.grid(row=0,column=0)
        self.canvass1.grid(row=0,column=1)

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

class bottom_frame(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)

class side_frame(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.__define_subframes()
        self.__align_subframes()

    def __define_subframes(self):
        self.base_generation_frame = base_generation_frame(self)
        self.circle_param_frame    = circle_param_frame(self)

    def __align_subframes(self):
        self.grid_columnconfigure(0,minsize=400)

        self.grid_rowconfigure(0,minsize=100)
        self.grid_rowconfigure(1,minsize=100)

        self.base_generation_frame.grid(row=0, column=0)
        self.circle_param_frame.grid(row=1,column=0)


class gui_object:
    def __init__(self):
        # All other 'global variabels' are initialized in the constructor.
        self.root = tk.Tk()
        self.root.wm_title("Dot Maker")

        self.__create_frames()
        self.__align_frames()
        self.root.mainloop()

    def __create_frames(self):
        self.root.wm_title("Dot Maker")
        self.canvass_master = canvass_master(self.root)
        self.bottom_frame   = bottom_frame(self.root)
        self.side_frame     = side_frame(self.root)

    def __align_frames(self):
        self.root.grid_columnconfigure(0,minsize=300)
        self.root.grid_columnconfigure(1,minsize=300)

        self.root.grid_rowconfigure(0,minsize=100)
        self.root.grid_rowconfigure(1,minsize=100)

        self.canvass_master.grid(row=0, column=0)
        self.bottom_frame.grid(row=1,column=1)
        self.side_frame.grid(row=0,column=1,rowspan=2)
