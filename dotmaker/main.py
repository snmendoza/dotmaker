import sys
from view import gui_object

def main():
    gui = gui_object()

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
