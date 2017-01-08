import view.ViewController as controller
import view.Subviews as subview
from view.AbstractViews import ParamFrameDefaults
import tkinter as tk
from PIL import ImageTk

class InputFrame(ParamFrameDefaults):
    def __init__(self, parent,controller):
        super(InputFrame,self).__init__(parent)
        self.__defineVars__(controller)
        self.__defineButtons__()
        self.__alignButtons__()

    def __defineVars__(self,controller):
        self.control = controller
        self.canvassParams = dict(width=50,height=50,bg='gray')
        self.canvassMethods = dict(imageMethod=self.drawImage,rectangleMethod=self.drawRectangle)
        self.column0 = []
        self.column1 = []

    def __defineButtons__(self):
        self.column0.append(tk.Label(self,text="Image Base Parameters",font=self.bigFont))
        self.column0.append(tk.Radiobutton(self, text="Black",**self.labelOptions,\
                          variable = self.control.getValue("inputType"), value="black",command=self.control.radioUpdate))
        self.column0.append(tk.Radiobutton(self, text="From Image",**self.labelOptions,\
                          variable = self.control.getValue("inputType"), value="image",command=self.control.radioUpdate))

        self.column1.append(tk.Button(self,text="Select Input Image",font=self.labelFont,width=14,command=self.control.loadImage))
        self.column1.append(self.control.createCanvas(self,self.canvassParams,self.canvassMethods))

    def __alignButtons__(self):
        self.grid_columnconfigure(0,minsize=100)
        self.grid_columnconfigure(1,minsize=150)

        self.grid_rowconfigure(0,minsize=30)
        self.grid_rowconfigure(1,minsize=30)
        self.grid_rowconfigure(2,minsize=30)
        self.grid_rowconfigure(3,minsize=30)

        self.column0[0].grid(row=0,column=0,columnspan=2,sticky='w')
        self.column0[1].grid(row=2,column=0,sticky='w')
        self.column0[2].grid(row=3,column=0,sticky='w')

        self.column1[0].grid(row=1,column=1,sticky='w')
        self.column1[1].grid(row=2,rowspan=2,column=1)
        self.drawRectangle()

    def drawImage(self,img):
        self.column1[1].delete("all")
        self.img = ImageTk.PhotoImage(img.resize((51,51)))
        self.column1[1].create_image(27,27,image=self.img)
        self.column1[1].update_idletasks()

    def drawRectangle(self):
        self.column1[1].delete("all")
        self.column1[1].create_rectangle(0, 0, 51, 51, fill='black')
        self.column1[1].update_idletasks()

class AnalysisFrame(ParamFrameDefaults):
    def __init__(self, parent,controller):
        super(AnalysisFrame,self).__init__(parent)
        self.__defineVars__(controller)
        self.__defineButtons__()
        self.__alignButtons__()

    def __defineVars__(self,controller):
        self.control = controller
        self.column0 = []
        self.column1 = []
        self.column2 = []

    def __defineButtons__(self):

        self.column0.append(tk.Label(self,text="Print Parameter Analysis",font=self.bigFont))
        self.column0.append(tk.Label(self,text="Numerical Opacity",**self.labelOptions))
        self.column0.append(tk.Label(self,text="Theoretical Opacity",**self.labelOptions))
        self.column0.append(tk.Label(self,text="Empirical Opacity",**self.labelOptions))

        self.column1.append(tk.Label(self,**self.longEntryOptions,\
                            textvariable=self.control.getTkVar('numericalOpacity')))
        self.column1.append(tk.Label(self,**self.longEntryOptions,\
                            textvariable=self.control.getTkVar('theoreticalOpacity')))
        self.column1.append(tk.Label(self,**self.longEntryOptions,\
                            textvariable=self.control.getTkVar('empiricalOpacity')))


    def __alignButtons__(self):
        self.grid_columnconfigure(0,minsize=50)
        self.grid_columnconfigure(1,minsize=100)

        self.grid_rowconfigure(0,minsize=30)
        self.grid_rowconfigure(1,minsize=20)
        self.grid_rowconfigure(2,minsize=20)
        self.grid_rowconfigure(3,minsize=20)

        self.column0[0].grid(row=0,column=0,columnspan=2,sticky='w')

        for i in range(1,len(self.column0)):
            self.column0[i].grid(row=i,column=0,sticky='w')

        for i in range(0,len(self.column1)):
            self.column1[i].grid(row=1+i,column=1,sticky='w')

class ActionFrame(tk.Frame):
    def __init__(self, parent,controller):
        tk.Frame.__init__(self,parent)
        self.__defineVars__(controller)
        self.__defineButtons__()
        self.__alignButtons__()

    def __defineVars__(self,controller):
        self.control      = controller
        self.paramFont    = ("Helvetica", 14)
        self.bigFont      = ("Helvetica", 18)

    def __defineButtons__(self):
        self.saveButton     = tk.Button(self,text="Save",font=self.bigFont,\
                            width=15,command=self.control.save)

        self.generateButton = tk.Button(self,text="Update Image",font=self.bigFont,\
                            width=15,command=self.control.generate)

    def __alignButtons__(self):
        self.grid_columnconfigure(0,minsize=300)
        self.grid_columnconfigure(1,minsize=300)
        self.grid_rowconfigure(0,minsize=50)

        self.saveButton.grid(column=0,row=0)
        self.generateButton.grid(column=1,row=0)

class PatternControlFrame(ParamFrameDefaults):
    def __init__(self, parent,controller):
        super(PatternControlFrame,self).__init__(parent)
        self.__defineVars__(controller)
        self.__defineButtons__()
        self.__alignButtons__()

    def __defineVars__(self,controller):
        self.control = controller

    def __defineButtons__(self):
        self.label   = tk.Label(self,text="Document Type",font=self.bigFont)
        button1param = dict(text="Multi Pattern Print ",width=20,font=self.labelFont)
        button2param = dict(text="Single Pattern Print",width=20,font=self.labelFont)
        buttons      = self.control.makeBooleanButtons(self,\
                                buttonParam=[dict(boundBool=False,param=button1param),\
                                             dict(boundBool=True,param=button2param)],\
                                boundvar=self.control.getKV('patternFrameType'),\
                                uicommand=self.changeButton)
        self.singleParamButton = buttons[0]
        self.multiParamButton  = buttons[1]

    def __alignButtons__(self):
        self.grid_columnconfigure(0,minsize=120,pad=5)
        self.grid_columnconfigure(1,minsize=120,pad=5)
        self.grid_rowconfigure(0,minsize=30,pad=5)

        self.label.grid(row=0,column=0,sticky='w')
        self.singleParamButton.grid(row=0,column=1,sticky='w')

    def changeButton(self,button):
        self.control.updateFrame()
        if button:
            self.multiParamButton.grid_forget()
            self.singleParamButton.grid(row=0,column=1,sticky='w')

        else:
            self.singleParamButton.grid_forget()
            self.multiParamButton.grid(row=0,column=1,sticky='w')

class CanvassFrame(ParamFrameDefaults):
    def __init__(self, parent,controller):
        super(CanvassFrame,self).__init__(parent)
        self.__defineVars__(controller)
        self.__defineButtons__()
        self.__alignButtons__()

    def __defineVars__(self,controller):
        self.control = controller
        self.control.update = self.update
        self.label_font = ("Helvetica", 14)

    def __defineButtons__(self):
        params   = dict(width=240, height=240, bg='gray')
        self.canvass1 = tk.Canvas(self,**params)
        self.canvass2 = tk.Canvas(self,**params)
        self.print_label  = tk.Label(self, text="Print View",font=self.label_font)
        self.cell_label   = tk.Label(self, text="Cell View",font=self.label_font)

    def __alignButtons__(self):
        self.grid_columnconfigure(0,minsize=300,pad=5)
        self.grid_columnconfigure(1,minsize=300,pad=5)

        self.grid_rowconfigure(0,minsize=30,pad=5)
        self.grid_rowconfigure(1,minsize=260)

        self.canvass1.grid(row=1,column=0)
        self.canvass2.grid(row=1,column=1)

        self.cell_label.grid(row=0,column=1)
        self.print_label.grid(row=0,column=0)

    def update(self,image,canvass):
        img = ImageTk.PhotoImage(image.resize((243,243)))
        if canvass is "cell":
            self.cell = img
            self.canvass2.delete("all")
            self.canvass2.create_image(120,120,image=self.cell)
            self.canvass2.update_idletasks()
        else:
            self.img = img
            self.canvass1.delete("all")
            self.canvass1.create_image(120,120,image=self.img)
            self.canvass1.update_idletasks()

class SideFrame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.__defineVars__(controller)
        self.__defineFrames__()
        self.__alignButtons__()

    def __defineVars__(self,controller):
        self.control = controller
        self.control.changeFrame = self.changeFrame

    def __defineFrames__(self):
        self.analysisFrame       = AnalysisFrame(self,self.control.getController("analysisControl"))
        self.InputFrame          = InputFrame(self,self.control.getController("inputControl"))
        self.multiParamFrame     = subview.MultiParamFrame(self,self.control.getController("multiPrintControl"))
        self.singleParamFrame    = subview.SingleParamFrame(self,self.control.getController("singlePrintControl"))
        self.controlFrame        = PatternControlFrame(self,self.control.getController("patternControl"))

    def __alignButtons__(self):
        self.grid_columnconfigure(0,minsize=300,pad=5)
        self.grid_columnconfigure(1,minsize=300,pad=5)
        self.grid_rowconfigure(0,minsize=30)
        self.grid_rowconfigure(1,minsize=260)
        self.grid_rowconfigure(2,minsize=80,pad=10)

        self.controlFrame.grid(row=0,column=0,columnspan=2)
        self.analysisFrame.grid(row=2,column=1,sticky='nw')
        self.InputFrame.grid(row=2,column=0,sticky='nw')
        self.changeFrame(True)

    def changeFrame(self,frame):
        if frame:
            self.singleParamFrame.grid_forget()
            self.multiParamFrame.grid(row=1,column=0,columnspan=2,sticky='w')
        else:
            self.multiParamFrame.grid_forget()
            self.singleParamFrame.grid(row=1,column=0,columnspan=2,sticky='w')


class MainView:
    def __init__(self):
        self.__defineVars__()
        self.__defineframes__()
        self.__alignFrames__()

    def __defineVars__(self):
        self.root = tk.Tk()
        self.mainController = controller.MainController()

    def __defineframes__(self):

        self.canvassFrame    = CanvassFrame(self.root,self.mainController.getController("canvassControl"))
        self.sideFrame       = SideFrame(self.root,self.mainController.getController("sideControl"))
        self.actionFrame     = ActionFrame(self.root,self.mainController.getController("actionControl"))

    def __alignFrames__(self):
        self.root.grid_columnconfigure(0,minsize=600)
        self.root.grid_columnconfigure(1,minsize=600)

        self.root.grid_rowconfigure(0,minsize=300)
        self.root.grid_rowconfigure(1,minsize=50)

        self.canvassFrame.grid(row=0, column=0)
        self.sideFrame.grid(row=0,rowspan=2,column=1,sticky='w')
        self.actionFrame.grid(row=1,column=0,sticky='w',padx=30)

    def run(self):
        self.root.mainloop()
