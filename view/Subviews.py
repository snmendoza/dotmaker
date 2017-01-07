import tkinter as tk
import pint
from view.AbstractViews import ParamFrameDefaults

class SingleParamFrame(ParamFrameDefaults):
    def __init__(self, parent,controller):
        super(SingleParamFrame,self).__init__(parent)
        self.__defineVars__(controller)
        self.__defineButtons__()
        self.__alignButtons__()

    def __defineVars__(self,controller):
        self.control = controller
        self.column0 = []
        self.column1 = []
        self.column2 = []
        self.column3 = []
        self.column4 = []
        self.column5 = []

    def __defineButtons__(self):
        #labels:
        self.column0.append(tk.Label(self, text="Print Parameters",font=self.bigFont))
        self.column0.append(tk.Label(self, text="Print Width:",**self.labelOptions))
        self.column0.append(tk.Label(self, text="Print height:",**self.labelOptions))
        self.column0.append(tk.Label(self, text="Dot Density:",**self.labelOptions))

        self.column3.append(tk.Label(self, text="Pattern Parameters",font=self.bigFont))
        self.column3.append(tk.Label(self, text="Print Type",**self.labelOptions))
        self.column3.append(tk.Label(self, text="Dot Separation:",**self.labelOptions))
        self.column3.append(tk.Label(self, text="Dot Radius:",**self.labelOptions))
        #entry:
        #Document Entrys
        self.column1.append(tk.Entry(self,**self.longEntryOptions,\
                            textvariable=self.control.getDocumentV('printHeight')))
        self.column1.append(tk.Entry(self,**self.longEntryOptions,\
                            textvariable=self.control.getDocumentV('printWidth')))
        self.column1.append(tk.Entry(self,**self.longEntryOptions,\
                            textvariable=self.control.getPatternV('density')))
        self.column4.append(tk.Entry(self,**self.longEntryOptions,\
                            textvariable=self.control.getPatternV('separation')))
        self.column4.append(tk.Entry(self,**self.longEntryOptions,\
                            textvariable=self.control.getPatternV('radius')))
        #option menu:
        self.column5.append(self.control.makeUnitMenu(self,basevar=self.control.getDocumentV('circleUnit'),\
                                  boundvar=[self.control.getPatternKV('radius'),\
                                  self.control.getPatternKV('separation')],\
                                  values=self.unitMenuOptions))
        self.column2.append(self.control.makeUnitMenu(self,basevar=self.control.getDocumentV("printUnit"),\
                                  boundvar=[self.control.getDocumentKV("printHeight"),\
                                  self.control.getDocumentKV("printWidth")],\
                                  values=self.unitMenuOptions))
        self.column2.append(self.control.makeUnitMenu(self,basevar=self.control.getDocumentV('densityUnit'),\
                                  boundvar=[self.control.getPatternKV('density')],values=self.unitMenuOptions))

        buttons      = self.control.makeBooleanButtons(self,\
                                buttonParam=[dict(boundBool=False,param=self.typeButtonOptions[0]),\
                                             dict(boundBool=True,param=self.typeButtonOptions[1])],\
                                boundvar=self.control.getDocumentKV('printType'),\
                                uicommand=self.__button_forget__)
        self.typePos = buttons[0]
        self.typeNeg = buttons[1]

        self.column4[0].bind('<Return>',lambda eff:self.control.update())
        self.column4[0].bind('<Tab>',lambda eff:self.control.update())
        self.column4[1].bind('<Return>',lambda eff:self.control.update())
        self.column4[1].bind('<Tab>',lambda eff:self.control.update())
        self.column1[2].bind('<Return>',lambda eff:self.control.update())
        self.column1[2].bind('<Tab>',lambda eff:self.control.update())

    def __alignButtons__(self):
        self.grid_columnconfigure(0,minsize=100)
        self.grid_columnconfigure(1,minsize=80)
        self.grid_columnconfigure(2,minsize=40)
        self.grid_columnconfigure(3,minsize=100)
        self.grid_columnconfigure(4,minsize=80)
        self.grid_columnconfigure(5,minsize=40)

        for i in range(0,5):
            self.grid_rowconfigure(i,minsize=30)

        self.column0[0].grid(row=0,column=0,columnspan=2,sticky='w')
        self.column3[0].grid(row=0,column=3,columnspan=2,sticky='w')

        #column0 labels
        for i in range(1,len(self.column0)):
            self.column0[i].grid(row=i,column=0,sticky='w')
        #column1 entrys
        for i in range(len(self.column1)):
            self.column1[i].grid(row=i+1,column=1,sticky='w')
        #column2 menu
        self.column2[0].grid(row=1,rowspan=2,column=2,sticky='w')
        self.column2[1].grid(row=3,column=2,sticky='w')

        #column3 labels
        for i in range(1,len(self.column3)):
            self.column3[i].grid(row=i,column=3,sticky='w')
        #column4 entrys
        for i in range(len(self.column4)):
            self.column4[i].grid(row=i+2,column=4,sticky='w')
        #column5 menu
        self.column5[0].grid(row=2,rowspan=2,column=5,sticky='w')
        self.__button_forget__(self.control.getDocumentV("printType"))

    def __button_forget__(self,btype):
        self.control.update()
        if btype:
            self.typeNeg.grid_forget()
            self.typePos.grid(row=1,column=4,sticky='w')
        else:
            self.typePos.grid_forget()
            self.typeNeg.grid(row=1,column=4,sticky='w')

class MultiParamFrame(ParamFrameDefaults):
    def __init__(self, parent,controller):
        super(MultiParamFrame,self).__init__(parent)
        self.__defineVars__(controller)
        self.__defineButtons__()
        self.__alignButtons__()

    def __defineVars__(self,controller):
        self.control = controller
        self.columnAlt = []
        self.column0 = []
        self.column1 = []
        self.column2 = []
        self.column3 = []
        self.column4 = []
        self.column5 = []
        self.column6 = []

    def __defineButtons__(self):
        #Categories:
        self.column0.append(tk.Label(self, text="Document Parameters",font=self.bigFont))
        self.column0.append(tk.Label(self, text="Print Type:",**self.labelOptions))
        self.column0.append(tk.Label(self, text="Document Width:",**self.labelOptions))
        self.column0.append(tk.Label(self, text="Document height:",**self.labelOptions))
        self.column0.append(tk.Label(self, text="Print Width:",**self.labelOptions))
        self.column0.append(tk.Label(self, text="Print height:",**self.labelOptions))
        self.column0.append(tk.Label(self, text="Print Margin:",**self.labelOptions))

        self.column3.append(tk.Label(self, text="Print Parameters",font=self.bigFont))

        self.column3.append(tk.Checkbutton(self, text="Dot Density:",\
            variable=self.control.getDocumentV("densitySelect"),\
            **self.checkButtonOptions,onvalue=True, offvalue=False,\
            command=lambda: self.control.checkButtonCall("density")))
        self.column3.append(tk.Checkbutton(self, text="Radius:",\
            variable=self.control.getDocumentV("radiusSelect"),\
            **self.checkButtonOptions,onvalue=True, offvalue=False,\
            command=lambda: self.control.checkButtonCall("radius")))
        self.column3.append(tk.Checkbutton(self, text="Separation:",\
            variable=self.control.getDocumentV("separationSelect"),\
            **self.checkButtonOptions,onvalue=True, offvalue=False,\
            command=lambda: self.control.checkButtonCall("separation")))

        self.column4.append(tk.Label(self, text="Start",**self.shortLabelOptions))
        self.column5.append(tk.Label(self, text="End",**self.shortLabelOptions))

        self.column1.append(tk.Entry(self,**self.longEntryOptions,\
                            textvariable=self.control.getDocumentV('documentWidth')))
        self.column1.append(tk.Entry(self,**self.longEntryOptions,\
                            textvariable=self.control.getDocumentV('documentHeight')))
        self.column1.append(tk.Entry(self,**self.longEntryOptions,\
                            textvariable=self.control.getDocumentV('printWidth')))
        self.column1.append(tk.Entry(self,**self.longEntryOptions,\
                            textvariable=self.control.getDocumentV('printHeight')))
        self.column1.append(tk.Entry(self,**self.longEntryOptions,\
                            textvariable=self.control.getDocumentV('printMargin')))

        self.column4.append(tk.Entry(self,**self.shortEntryOptions,\
                            textvariable=self.control.getPatternV(1,'density')))
        self.column4.append(tk.Entry(self,**self.shortEntryOptions,\
                            textvariable=self.control.getPatternV(1,'radius')))
        self.column4.append(tk.Entry(self,**self.shortEntryOptions,\
                            textvariable=self.control.getPatternV(1,'separation')))

        self.column5.append(tk.Entry(self,**self.shortEntryOptions,\
                            textvariable=self.control.getPatternV(2,'density')))
        self.column5.append(tk.Entry(self,**self.shortEntryOptions,\
                            textvariable=self.control.getPatternV(2,'radius')))
        self.column5.append(tk.Entry(self,**self.shortEntryOptions,\
                            textvariable=self.control.getPatternV(2,'separation')))

        self.column2.append(self.control.makeUnitMenu(self,basevar=self.control.getDocumentV('documentUnit'),\
                                  boundvar=[self.control.getDocumentKV('documentWidth'),self.control.getDocumentKV('documentHeight')],\
                                  values=self.unitMenuOptions))
        self.column2.append(self.control.makeUnitMenu(self,basevar=self.control.getDocumentV('printUnit'),\
                                  boundvar=[self.control.getDocumentKV('printWidth'),self.control.getDocumentKV('printHeight'),\
                                        self.control.getDocumentKV('printMargin')],\
                                  values=self.unitMenuOptions))
        self.column6.append(self.control.makeUnitMenu(self,basevar=self.control.getDocumentV('densityUnit'),\
                                  boundvar=[self.control.getPatternKV(1,'density'),self.control.getPatternKV(2,'density')],\
                                  values=self.unitMenuOptions))
        self.column6.append(self.control.makeUnitMenu(self,basevar=self.control.getDocumentV('circleUnit'),\
                                  boundvar=[self.control.getPatternKV(1,"radius"),self.control.getPatternKV(2,"radius"),\
                                        self.control.getPatternKV(1,"separation"),self.control.getPatternKV(2,"separation")],\
                                  values=self.unitMenuOptions))

        buttons      = self.control.makeBooleanButtons(self,\
                                buttonParam=[dict(boundBool=False,param=self.typeButtonOptions[0]),\
                                             dict(boundBool=True,param=self.typeButtonOptions[1])],\
                                boundvar=self.control.getDocumentKV('printType'),\
                                uicommand=self.__button_forget__)
        self.typePos = buttons[0]
        self.typeNeg = buttons[1]

        for i in range(1,3):
            self.column4[i].bind('<Return>',lambda eff:self.control.update())
            self.column4[i].bind('<Tab>',lambda eff:self.control.update())
            self.column5[i].bind('<Return>',lambda eff:self.control.update())
            self.column5[i].bind('<Tab>',lambda eff:self.control.update())

    def __alignButtons__(self):
        self.grid_columnconfigure(0,minsize=100)
        self.grid_columnconfigure(1,minsize=80)
        self.grid_columnconfigure(2,minsize=40)
        self.grid_columnconfigure(3,minsize=40)
        self.grid_columnconfigure(4,minsize=40)
        self.grid_columnconfigure(5,minsize=40)
        for i in range(0,len(self.column0)):
            self.grid_rowconfigure(i,minsize=30)

        self.column0[0].grid(row=0,column=0,columnspan=2,sticky='w')
        self.column3[0].grid(row=0,column=3,columnspan=2,sticky='w')

        self.column2[0].grid(row=2,column=2,rowspan=2,sticky='w')
        self.column2[1].grid(row=4,column=2,rowspan=3,sticky='w')
        self.column4[0].grid(row=1,column=4,sticky='w')
        self.column5[0].grid(row=1,column=5,sticky='w')
        #static:

        for i in range(1,len(self.column0)):
            self.column0[i].grid(row=i,column=0,sticky='w')

        for i in range(0,len(self.column1)):
            self.column1[i].grid(row=i+2,column=1,sticky='w')

        for i in range(1,len(self.column3)):
            self.column3[i].grid(row=i+1,column=3,sticky='w')

        for i in range(0,len(self.column4)):
            self.column4[i].grid(row=i+1,column=4,sticky='w')
            self.column5[i].grid(row=i+1,column=5,sticky='w')

        self.column6[0].grid(row=2,column=6,sticky='w')
        self.column6[1].grid(row=3,rowspan=2,column=6,sticky='w')

        self.typePos.grid(row=1,column=1,sticky='w')

    def __button_forget__(self,btype):
        self.control.update()
        if btype:
            self.typeNeg.grid_forget()
            self.typePos.grid(row=1,column=1,sticky='w')
        else:
            self.typePos.grid_forget()
            self.typeNeg.grid(row=1,column=1,sticky='w')
