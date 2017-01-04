import tkinter as tk

class ParamFrameDefaults(tk.Frame):
    def __init__(self,parent):
        tk.Frame.__init__(self,parent)
        self.bigFont            = ("Helvetica", 18)
        self.labelFont          = ("Helvetica", 14)
        self.unitMenuOptions    = [chr(956)+'m','mm','cm','in']
        self.optionMenuParams   = dict(width=4)
        self.shortLabelOptions  = dict(font=self.labelFont,width=5,anchor='w')
        self.labelOptions       = dict(font=self.labelFont,width=15,anchor='w')
        self.longEntryOptions   = dict(font=self.labelFont,width=9)
        self.shortEntryOptions  = dict(font=self.labelFont,width=5)
        self.checkButtonOptions = dict(font=self.labelFont,width=12)
        self.typeButtonOptions  = (dict(text="Positive",width=7,font=self.labelFont),\
                                  dict(text="Negative",width=7,font=self.labelFont))
