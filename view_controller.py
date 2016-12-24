#!/usr/bin/python
import tkinter as tk
import tkinter.filedialog
import PIL.Image
from PIL import ImageTk, Image
import pint
import math
import model.Model_Controller as model
##
#notes:
#-analyze
#-autodraw unit cell
#
def convert_unit(ureg,prevnumber=None,prevunit=None,newunit=None):
    return str(ureg(prevnumber.get() + prevunit.get()).to(newunit).magnitude)

def normalize_unit(ureg,prevnumber=None,prevunit=None):
    return str(ureg(prevnumber.get() + prevunit.get()).to("cm").magnitude)

class base_generation_frame(tk.Frame):
    def __init__(self, parent,command_dict):
        tk.Frame.__init__(self, parent)
        self.__define_vars(command_dict)
        self.__define_buttons()
        self.__align_buttons()


    def get_var_params(self):
        if self.gen_option==1:
            inpath = None
        else:
            inpath = self.inpath

        return dict(input_file=inpath,
                    height=(self.height.get(),self.unit.get()),
                    width=(self.width.get(),self.unit.get()))

    def __define_vars(self,command_dict):
        self.update_unit_cell_cmd = command_dict.get("generate_canvass")
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
        self.input_lab = tk.Label(self, text="Input file:", font=self.label_font)
        self.input_file_lab = tk.Label(self, textvariable=self.inpath, font=self.label_font, width=15, anchor='e', justify='right')
        #entry:
        self.width_ent  = tk.Entry(self, font=self.entry_font,width=5,\
                            textvariable=self.width)
        self.height_ent = tk.Entry(self,font=self.entry_font,width=5,\
                            textvariable=self.height)
        #Generation Options
        self.base_but   = tk.Radiobutton(self, text='From base file',font=self.label_font,\
                          variable = self.gen_option, value=2)
        self.gen_but    = tk.Radiobutton(self, text='Generated',font=self.label_font,\
                          variable = self.gen_option, value=1)
        #option menu:
        self.dot_menu   = tk.OptionMenu(self, self.temp_unit, \
                    *[chr(956)+'m','mm','cm','in'], command=self.__dim_update)
        #buttons
        self.browse_in_butt = tk.Button(self, text='Browse', font=self.label_font, command=self.__browsein)


    def __align_buttons(self):
        self.grid_columnconfigure(0,minsize=100)
        self.grid_columnconfigure(1,minsize=100)
        self.grid_columnconfigure(2,minsize=50)

        self.grid_rowconfigure(0,minsize=50)
        self.grid_rowconfigure(1,minsize=30)
        self.grid_rowconfigure(2,minsize=30)

        self.dot_menu.grid(row=2,column=2,sticky='w')

        self.width_lab .grid(row=2,column=0,sticky='w')
        self.height_lab.grid(row=3,column=0,sticky='w')

        self.width_ent.grid(row=2,column=1,sticky='w')
        self.height_ent.grid(row=3,column=1,sticky='w')

        self.base_but.grid(row=1,column=0,sticky='w')
        self.gen_but.grid(row=1,column=2,sticky='w')

        self.input_lab.grid(row=0, column=0, sticky='w')
        self.input_file_lab.grid(row=0, column=1, sticky='w')

        self.browse_in_butt.grid(row=0, column=2, sticky='w')


    def __dim_update(self,update):
        self.height.set(convert_unit(self.ureg,self.height,self.unit,update))
        self.width.set(convert_unit(self.ureg,self.width,self.unit,update))
        self.unit.set(update)

    def __browsein(self):
        """get file location string, display string, open image, make
        make resized image, display both, save both for future ref"""
        I = str(tk.filedialog.askopenfilename())
        self.inpath.set(I)
        self.gen_option=0

class circle_param_frame(tk.Frame):
    def __init__(self, parent,command_dict):
        tk.Frame.__init__(self, parent)
        self.__define_vars(command_dict)
        self.__define_buttons()
        self.__align_buttons()

    def get_var_params(self):
        return dict(px_cm=(self.pixels_per_unit_value.get(),self.pixels_per_unit_unit.get()),
                    separation=(self.separation.get(),self.unit.get()),
                    radius=(self.radius.get(),self.unit.get()),
                    is_positive=self.pos.get())

    def __define_vars(self,command_dict):
        self.update_unit_cell_cmd = command_dict.get("generate_canvass")
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
        self.unit.set('cm')

    def __define_buttons(self):
        #labels:
        self.density_lab  = tk.Label(self, text="Dot Density:",font=self.label_font)
        self.dot_sep_lab  = tk.Label(self, text="Dot Separation:",font=self.label_font)
        self.dot_rad_lab  = tk.Label(self, text="Dot Radius:",font=self.label_font)
        #entry:
        self.density_ent  = tk.Entry(self,font=self.entry_font,width=5,\
                            textvariable=self.pixels_per_unit_value)
        self.density_ent.bind('<Return>',lambda eff:self.__update_cell())
        self.dot_sep_ent  = tk.Entry(self, font=self.entry_font,width=5,\
                            textvariable=self.separation)
        self.dot_sep_ent.bind('<Return>',lambda eff:self.__update_cell())
        self.dot_rad_ent  = tk.Entry(self, font=self.entry_font,width=5,\
                            textvariable=self.radius)
        self.dot_rad_ent.bind('<Return>',lambda eff:self.__update_cell())
        #option menu:
        self.dot_menu     = tk.OptionMenu(self, self.temp_unit2, *[chr(956)+'m','mm','cm','in'], command=self.__circle_update)
        self.density_menu = tk.OptionMenu(self, self.temp_unit1, *[chr(956)+'m','mm','cm','in'], command=self.__density_update)
        #radiobuttons:
        self.pos_but      = tk.Radiobutton(self, text="Positive Print", font=self.label_font, \
            value=True,  variable=self.pos, command=self.__update_cell)
        self.neg_but      = tk.Radiobutton(self, text="Negative Print", font=self.label_font, \
            value=False, variable=self.pos, command=self.__update_cell)

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

        self.pos_but.grid(row=3,column=0,sticky='w')
        self.neg_but.grid(row=3,column=1,sticky='w')

    def __density_update(self,update):
        self.pixels_per_unit_value.set(convert_unit(self.ureg, \
            self.pixels_per_unit_value,self.pixels_per_unit_unit,update))
        self.pixels_per_unit_unit.set(update)

    def __circle_update(self,update):
        self.radius.set(convert_unit(self.ureg,self.radius,self.unit,update))
        self.separation.set(convert_unit(self.ureg,self.separation,self.unit,update))
        self.unit.set(update)

    def __update_cell(self):
        self.update_unit_cell_cmd("cell")

class canvass_master(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self,parent)
        self.__define_vars()
        self.__define_buttons()
        self.__align_buttons()

    def __define_vars(self):
        self.image1 = None
        self.image2 = None
        self.label_font = ("Helvetica", 14)

    def update_canvass(self,image,canvass):
        if canvass is "cell":
            self.image2 = ImageTk.PhotoImage(image.resize((240,240)))
            self.canvass2.create_image(120,120, image=self.image2)
        else:
            self.image1 = ImageTk.PhotoImage(image.resize((240,240)))
            self.canvass1.create_image(120,120, image=self.image1)

    def __define_buttons(self):
        self.canvass1 = tk.Canvas(self, width=240, height=240, bg='gray')
        self.canvass2 = tk.Canvas(self, width=240, height=240, bg='gray')
        self.print_label  = tk.Label(self, text="Print View",font=self.label_font)
        self.cell_label  = tk.Label(self, text="Cell View",font=self.label_font)

    def __align_buttons(self):
        self.grid_columnconfigure(0,minsize=330,pad=5)
        self.grid_columnconfigure(1,minsize=330,pad=5)

        self.grid_rowconfigure(0,minsize=30,pad=5)
        self.grid_rowconfigure(1,minsize=260)

        self.canvass1.grid(row=1,column=0)
        self.canvass2.grid(row=1,column=1)

        self.cell_label.grid(row=0,column=1)
        self.print_label.grid(row=0,column=0)

class gen_frame(tk.Frame):
    def __init__(self, parent, command_dict):
        tk.Frame.__init__(self, parent)
        self.__define_vars(command_dict)
        self.__define_buttons()
        self.__align_buttons()

    def get_save_filepath(self):
        if self.out_directory==None:
            return None

        else:
            return self.out_directory + "/" + self.filenamevar.get()

    def __define_vars(self,command_dict):
        self.out_directory = None

        self.filepathvar = tk.StringVar()
        self.filepathvar.set("Save Directory:")
        self.filenamevar = tk.StringVar()
        self.filenamevar.set("dotmaker pattern")

        self.__generate_canvass = command_dict.get("generate_canvass")
        self.__save_cmd = command_dict.get("save")
        self._label_font = ("Helvetica", 11)
        self._button_font = ("Helvetica", 11)

    def __define_buttons(self):
        self.file_out = tk.Button(self, text='Browse', font=self._label_font,width=15, command=self.__setpath)
        self.file_out_path = tk.Label(self, textvariable=self.filepathvar, font=self._label_font)

        self.file_name_lab = tk.Label(self, text="Appended File Name",font=self._label_font)
        self.file_name_append = tk.Entry(self, textvariable=self.filenamevar,font=self._label_font,width=15)

        self.gen_button = tk.Button(self, text="Generate", font = self._label_font,width=15,\
            command=self.__generate)
        self.save_button = tk.Button(self, text="Save", font=self._label_font,width=15,\
            command=self.__save_cmd)

    def __generate(self):
        self.__generate_canvass("full")

    def __align_buttons(self):
        self.grid_columnconfigure(0,minsize=150)
        self.grid_columnconfigure(1,minsize=30)

        self.grid_rowconfigure(0,minsize=30)
        self.grid_rowconfigure(1,minsize=30)
        self.grid_rowconfigure(2,minsize=30)

        self.file_name_lab.grid(row=0,column=0,sticky='w')
        self.file_name_append.grid(row=0,column=1,sticky='w')

        self.file_out_path.grid(row=1,column=0,sticky='w')
        self.file_out.grid(row=1,column=1,sticky='w')

        self.gen_button.grid(row=2,column=0,sticky='w')
        self.save_button.grid(row=2,column=1,sticky='w')

    def __setpath(self):
        I = str(tk.filedialog.askdirectory())
        self.out_directory=I
        l = len(I)
        self.filepathvar.set("Save Directory:" + I[l-10:l])

class side_frame(tk.Frame):
    def __init__(self, parent, command_dict):
        tk.Frame.__init__(self, parent)
        self.__define_subframes(command_dict)
        self.__align_subframes()

    def __define_subframes(self,command_dict):
        self.generate_frame        = gen_frame(self,command_dict)
        self.base_generation_frame = base_generation_frame(self,command_dict)
        self.circle_param_frame    = circle_param_frame(self,command_dict)

    def __align_subframes(self):
        self.grid_columnconfigure(0,minsize=200)

        self.grid_rowconfigure(0,minsize=100)
        self.grid_rowconfigure(1,minsize=100)
        self.grid_rowconfigure(2,minsize=100)

        self.base_generation_frame.grid(row=0, column=0)
        self.circle_param_frame.grid(row=1,column=0)
        self.generate_frame.grid(row=2,column=0)

    def get_save_filepath(self):
        return self.generate_frame.get_save_filepath()

    def get_vars(self):
        dict1 = self.base_generation_frame.get_var_params()
        dict2 = self.circle_param_frame.get_var_params()
        return {**dict1, **dict2}

class View_Controller:
    def __init__(self):
        # All other 'global variabels' are initialized in the constructor.
        self.root = tk.Tk()
        self.__create_frames()
        self.__align_frames()
        self.root.mainloop()

    def __create_frames(self):
        self.root.wm_title("Dot Maker")
        commands_dict = dict(
            generate_canvass  = self.generate_canvass,\
            get_cell_analysis = self.analyze_unit_cell,\
            save=self.__save)
        self.canvass_master = canvass_master(self.root)
        self.side_frame     = side_frame(self.root,commands_dict)

    def __align_frames(self):
        self.root.grid_columnconfigure(0,minsize=300)
        self.root.grid_columnconfigure(1,minsize=300)

        self.root.grid_rowconfigure(0,minsize=100)

        self.canvass_master.grid(row=0, column=0)
        self.side_frame.grid(row=0,column=1)

    def __save(self):
        if self.img_model!=None:
            vars_dict = self.side_frame.get_vars()
            filepath = self.side_frame.get_save_filepath()
            if filepath!=None:
                px_cm = vars_dict.get("px_cm")
                sep = vars_dict.get("separation")
                radius = vars_dict.get("radius")

                filepath = filepath + "_r_:" + str(radius[0]) + str(radius[1])
                filepath = filepath + "_s_:" + str(sep[0]) + str(sep[1])
                filepath = filepath + "_pp_:" + str(px_cm[0]) + str(px_cm[1])
                filepath = filepath + ".png"
                print(filepath)
                self.png.save(filepath)

    def generate_canvass(self,canvass):
        self.canvass_master.update_canvass(self.get_png(canvass),canvass)

    def get_png(self,png_type):
        return model.single_pattern(pattern_type=png_type,params=self.side_frame.get_vars()):

    def analyze_unit_cell(self):
        return model.anayze_unit_cell(self.side_frame.get_vars()):
