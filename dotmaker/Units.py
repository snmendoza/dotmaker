import pint
class gui_object:
    def __init__(self, var):
        # All other 'global variabels' are initialized in the constructor.
        self.root = Tk()

        ###setup variables as tk var, set value
        self.var = var

        x       = IntVar()
        y       = IntVar()
        pos     = BooleanVar()
        dpcm    = IntVar()
        sep     = IntVar()
        re      = IntVar()


        x       = 100
        y       = 100
        pos     = True
        dpcm    = 1000
        sep     = 200
        r       = 70

        dim = []
        dim.append(x)
        dim.append(y)
        self.resep_units = StringVar()
        self.resep_units.set("1")
        self.var.set_dimensions(dim)
        self.var.set_separation(sep)
        self.var.set_radius(r)
        self.var.set_positive(pos)
        self.var.set_dots_per_cm(dpcm)
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

    def __generate_image(self):
        imageGenerator = png_maker(self.var)
        pngObject = imageGenerator.createpng()
        draw_canvas(pngObject)
        ######################################
        ### pngOBJ is a PNG OBJ!!!!     ######
        ######################################
        ### put it into the canvas!     ######
        ######################################
# Generates user prompt for input file directory
