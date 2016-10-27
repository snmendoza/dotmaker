def __generate_image(self):
    """method that does everything needed to actually create the png"""

    #standardize dpi measurement to px per cm
    px_per_cm      = self.ureg(str(self.pixels_per_unit_value.get()) + \
                 self.pixels_per_unit_unit.get()).to("cm").magnitude
    # positive vs negative print
    pos        = self.is_positive.get()
    #standardize height measurement to cm
    height     = self.ureg(str(self.height.get())   + \
                 self.dimunits.get()).to("cm").magnitude
    #standardize width measurement to cm
    width      = self.ureg(str(self.width.get())     + \
                 self.dimunits.get()).to("cm").magnitude
    #standardize radius measurement to cm
    radius     = self.ureg(str(self.radius.get())    + \
                 self.resep_old_units.get()).to("cm").magnitude
    #standardize separation measurement to cm
    separation = self.ureg(str(self.separation.get()) + \
                 self.resep_old_units.get()).to("cm").magnitude

    #Now that all the salient variables are converted to px per cm or cm,
    #to find the remaining px values all we do is multiply by px_cm
    var_container = image_vars()
    var_container.set_height(       int(float(  height      * px_per_cm  )))
    var_container.set_width(        int(float(  width       * px_per_cm  )))
    var_container.set_separation(   int(float(  separation  * px_per_cm  )))
    var_container.set_radius(       int(float(  radius      * px_per_cm  )))
    var_container.set_positive(pos)

    if self.from_Base_File:
        var_container.set_image_file(None)
    else:
        var_container.set_image_file(self.inpath)

    imageGenerator = png_maker(var_container)
    pngObject = imageGenerator.createpng()
    self.__draw_canvas(pngObject)
