import sys
from png_interface import png_maker
from GUI import gui_object
from containers import image_vars

def main():
    var_container = image_vars()
    gui = gui_object(var_container)


main()
