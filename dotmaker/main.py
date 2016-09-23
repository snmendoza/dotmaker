import sys
from png_interface import png_maker
from GUI import gui_object
from containers import image_vars

def main():
    var_container = image_vars()
    gui = gui_object(var_container)

def __savetofile(self):

    filename = "Type__" + self.isNeg + ""\
                "dot_size__" \
                "" + str(int(self.dotsize*10000/(self.px_cm))) + "" \
                "_dot_spacing__" \
                "" + str(int(self.dotspacing*10000/(self.px_cm))) + ".png"
    if self.validFile:
        path = os.path.split(self.pngFilePath)
        path = path[0]
    else:
        path = self.pngFilePath
    path = os.path.join(path,filename)
    self.pngobj.img.save(path,"png")
main()
