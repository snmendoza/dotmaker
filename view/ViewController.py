#!/usr/bin/python
import tkinter as tk
import tkinter.filedialog as dialog
import PIL.Image
from PIL import ImageTk, Image
import pint
import math
import model.ModelController as model
##
#notes:
#-analyze
#-autodraw unit cell
#
def convert_unit(ureg,prevvar=None,prevunit=None,newunit=None):
    newvar = str(ureg(prevvar.get() + prevunit.get()).to(newunit).magnitude)
    return newvar

def normalize_unit(ureg,prevnumber=None,prevunit=None):
    return str(ureg(prevnumber.get() + prevunit.get()).to("cm").magnitude)

class ParamAccess:
    def __init__(self):
        self.varDict = None
        self.unitMenuControllers     = []
        self.booleanValueControllers = []

    def setTkValue(self,key,value):
        if key in self.varDict:
            self.varDict[key].set(value)

    def setValue(self,key,value):
        if key in self.varDict:
            self.varDict[key]=value

    def getValue(self,key):
        return self.varDict[key]

    def makeUnitMenu(self,frame,basevar=None,boundvar=None,values=None):
        subdict = { key:value for key,value in self.varDict.items() if key in boundvar }
        uControl = UnitValueController(start=self.varDict[basevar],variables=subdict)
        self.unitMenuControllers.append(uControl)
        return tk.OptionMenu(frame,self.varDict[basevar],*values,command=uControl.updateUnit)

    def makeBooleanButtons(self,frame,buttons=None,method=None,variable=""):
        b = []
        for entry in buttons.keys():
            cont = BoolValueController(self.varDict[variable],buttons[entry]["value"],method)
            b.append(tk.Button(frame,**buttons[entry]["param"],command=cont.updateValue))
            self.booleanValueControllers.append(cont)

        return b

class BoolValueController:
    def __init__(self,variable,value,method):
        self.var   = variable
        self.value = value
        self.method = method

    def updateValue(self):
        self.var.set(self.value)
        self.method(self.var.get())

class UnitValueController:
    def __init__(self,start=None,variables=None):
        self.ureg = pint.UnitRegistry()
        self.variables = variables
        self.startUnit = tk.StringVar()
        self.startUnit.set(start.get())

    def updateUnit(self,unit):
        for key in self.variables.keys():
            if self.variables[key].get() is not "":
                self.variables[key].set(convert_unit(self.ureg,prevvar=self.variables[key],\
                prevunit=self.startUnit,newunit=unit))

        self.startUnit.set(unit)

class SinglePrintController(ParamAccess):
    def __init__(self,unitCellUpdate):
        super(SinglePrintController, self).__init__()
        self.ureg = pint.UnitRegistry()
        self.__defineVars__(unitCellUpdate)

    def __defineVars__(self,update):
        self.update = update
        self.varDict = dict(
            radius         = tk.StringVar(),\
            circleUnit     = tk.StringVar(),\
            densityUnit    = tk.StringVar(),\
            separation     = tk.StringVar(),\
            density        = tk.StringVar(),\
            documentWidth  = tk.StringVar(),\
            documentHeight = tk.StringVar(),\
            documentUnit   = tk.StringVar(),\
            printType      = tk.BooleanVar())

    def getParams(self):
        return self.varDict

class MultiPrintController(ParamAccess):
    def __init__(self,update):
        super(MultiPrintController, self).__init__()
        self.ureg = pint.UnitRegistry()
        self.__defineVars__(update)

    def __defineVars__(self,update):
        self.update=update
        self.varDict = dict(
            radius1      = tk.StringVar(),\
            separation1  = tk.StringVar(),\
            density1     = tk.StringVar(),\
            radius2      = tk.StringVar(),\
            separation2  = tk.StringVar(),\
            density2     = tk.StringVar(),\
            densityUnit = tk.StringVar(),\
            circleUnit  = tk.StringVar(),\
            documentWidth= tk.StringVar(),\
            documentHeight=tk.StringVar(),\
            documentUnit= tk.StringVar(),\
            printWidth  = tk.StringVar(),\
            printHeight = tk.StringVar(),\
            printUnit   = tk.StringVar(),\
            staticVar   = tk.StringVar(),\
            staticUnit  = tk.StringVar(),\
            printMargin = tk.StringVar(),\
            printType   = tk.BooleanVar())
        self.checkDict  = dict(\
            density     = tk.StringVar(),\
            radius      = tk.StringVar(),\
            separation  = tk.StringVar())
        self.checkStates=[]
        self.checkDict["density"].set("0")
        self.checkDict["radius"].set("0")
        self.checkDict["separation"].set("0")

    def checkButtonCall(self,var):
        if self.checkDict[var].get() is not "0":
            if len(self.checkStates) == 2:
                state = self.checkStates.pop(0)
                self.checkDict[state].set("0")
                state = state + "2"
                self.varDict[state].set("")

            self.checkStates.append(var)

    def checkVar(self,key):
        return self.checkDict[key]

    def getParams(self):
        pass

class AnalysisController(ParamAccess):
    def __init__(self):
        super(AnalysisController, self).__init__()
        self.__defineVars__()

    def __defineVars__(self):
        self.varDict = dict(\
            numericalOpacity    = tk.StringVar(),\
            theoreticalOpacity  = tk.StringVar(),\
            empiricalOpacity    = tk.StringVar())

class PatternController(ParamAccess):
    def __init__(self):
        super(PatternController, self).__init__()
        self.__defineVars__()

    def __defineVars__(self):
            self.varDict = dict(patternType = tk.BooleanVar())

class InputController(ParamAccess):
    def __init__(self,update):
        super(InputController, self).__init__()
        self.__defineVars__(update)

    def __defineVars__(self,update):
        self.update = update
        self.varDict = dict(InputType= tk.IntVar(),\
                            InputImage=None)
        self.canvas = None
        self.file_opt = dict(defaultextension='.png',\
                             filetypes= [('png files', '.png')],\
                             message="Select a Source .png Image")

    def radioUpdate(self):
        self.canvas.delete("all")
        if self.getValue("InputType").get()==1:
            self.rectangleMethod()

        else:
            if self.getValue("InputImage") is None:
                self.loadImage()
            img = self.getValue("InputImage").copy()
            self.imageMethod(img)

        self.update()

    def createCanvas(self,frame,canvassParams,canvassMethods):
        self.imageMethod = canvassMethods["imageMethod"]
        self.rectangleMethod = canvassMethods["rectangleMethod"]
        self.canvas = tk.Canvas(frame,**canvassParams)
        return self.canvas

    def loadImage(self):
        img = PIL.Image.open(dialog.askopenfilename(**self.file_opt))
        img = img.convert("RGBA")
        self.setValue("InputImage",img.copy())

class SideController:
    def __init__(self, modelControl):
        self.__defineVars__(modelControl)

    def __defineVars__(self,modelControl):
        self.modelControl = modelControl
        self.controllers = dict(singlePrintControl=SinglePrintController(self.updateUnitCell),\
                               multiPrintControl=MultiPrintController(self.updateUnitCell),\
                               analysisControl=AnalysisController(),\
                               inputControl=InputController(self.updateUnitCell),\
                               patternControl=PatternController())

        self.singleDefaults = dict(radius='0.1',separation='0.3',density='500',printType=False,documentHeight='3',\
            documentWidth='3',circleUnit='mm',densityUnit='cm',documentUnit='cm')

        self.printDefaults = dict(patternType=True)
        self.inputDefaults = dict(InputType=1)
        self.multiDefaults = dict(radius1='0.05',radius2='0.1',separation1='0.4',\
            separation2='0.3',circleUnit='mm',\
            density1='500',density2="600",densityUnit='cm',printType=False,\
            documentHeight='11',documentWidth='8.5',documentUnit='in',\
            printHeight='3',printWidth='3',printUnit='cm',printMargin='0.1',marginUnit='cm')

        self.__setControllerDefaults__(self.controllers["inputControl"],self.inputDefaults)
        self.__setControllerDefaults__(self.controllers["multiPrintControl"],self.multiDefaults)
        self.__setControllerDefaults__(self.controllers["singlePrintControl"],self.singleDefaults)
        self.__setControllerDefaults__(self.controllers["patternControl"],self.printDefaults)

    def __setControllerDefaults__(self,controller,defaults):
        for key in defaults.keys():
            controller.setTkValue(key,defaults[key])

    def getController(self,controller):
        return self.controllers.get(controller)

    def getImage(self):
        if self.controllers["inputControl"].getValue("InputType").get()==2:
            return self.controllers["inputControl"].getValue("InputImage")
        else:
            return None

    def getParamType(self):
        return self.controllers["patternControl"].getValue("patternType").get()

    def getParams(self):
        if self.controllers["patternControl"].getValue("patternType").get():
             return self.controllers["singlePrintControl"].getParams()
        else:
             return self.controllers["multiPrintControl"].getParams()

    def updateUnitCell(self):
        self.modelControl.updateUnitCell(\
        self.controllers["patternControl"].getValue("patternType").get())

class CanvassController:
    def __init__(self, modelControl):
        self.__defineVars__(modelControl)

    def __defineVars__(self,modelControl):
        self.modelControl = modelControl

    def updateCanvass(self,image,canvass):
        self.update(image,canvass)

class ActionController:
    def __init__(self,modelControl):
        self.model = modelControl

    def save(self):
        img = self.model.save()
        filename = dialog.asksaveasfilename()
        img.save(filename + ".png")

    def generate(self):
        self.model.updatePrintView()

class MainController:
    def __init__(self):
        self.__defineVars__()

    def __defineVars__(self):
        self.modelControl = model.ModelControl()
        self.controller = dict(canvassControl=CanvassController(self.modelControl),\
                               actionControl=ActionController(self.modelControl),\
                               sideControl=SideController(self.modelControl))
        self.modelControl.action=self.getController("actionControl")
        self.modelControl.params=self.getController("sideControl")
        self.modelControl.display=self.getController("canvassControl")

    def getController(self,controllerType):
        return self.controller.get(controllerType)
