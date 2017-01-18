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

def dictSet(dict1, dict2):
    for key in dict1.keys():
        if key in dict2.keys():
            dict2[key].set(dict1[key])

class WidgetVarIntegration:
    def __init__(self):
        self.linkedVariables = {}
        self.unitMenuControllers     = []
        self.booleanValueControllers = []

    def makeInverseUnitMenu(self,frame,basevar=None,boundvar=None,values=None):
        for entry in boundvar:
            self.linkedVariables[entry[0]] = entry[1]

        uControl = InverseUnitValueController(start=basevar,boundvar=boundvar)
        self.unitMenuControllers.append(uControl)
        return tk.OptionMenu(frame,basevar,*values,command=uControl.updateUnit)

    def makeUnitMenu(self,frame,basevar=None,boundvar=None,values=None):
        '''makes a unit menu based on a base tkvariable and desired bound fields
                basevar= the base tkvariable
                boundvar= bound tkvariables to update when basevar changes
                values= units selectable from the menu'''
        for entry in boundvar:
            self.linkedVariables[entry[0]] = entry[1]

        uControl = UnitValueController(start=basevar,boundvar=boundvar)
        self.unitMenuControllers.append(uControl)
        return tk.OptionMenu(frame,basevar,*values,command=uControl.updateUnit)

    def makeBooleanButtons(self,frame,buttonParam=None,boundvar=None,uicommand=None):
        '''makes a boolean button pair based on a base tkvariable and desired bound fields
                buttonParam= a list of dicts. inner dict needs primitive keys
                        boundBool = the beginning state.
                        param = a dict of params for the tk.Button
                    outer list should contain only two inner dicts
                boundvar= bound tkvariable to update when clicked
                uicommand= a ui command to call when button is clicked'''
        b=[]
        self.linkedVariables[boundvar[0]] = boundvar[1]
        for e in range(len(buttonParam)):
            cont = BoolValueController(boundvar[1],buttonParam[e]["boundBool"],uicommand)
            b.append(tk.Button(frame,**buttonParam[e]["param"],command=cont.updateValue))
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
    def __init__(self,start=None,boundvar=None):
        self.ureg = pint.UnitRegistry()
        self.variables = {}
        for entry in boundvar:
            self.variables[entry[0]] = entry[1]

        self.startUnit = tk.StringVar()
        self.startUnit.set(start.get())

    def updateUnit(self,unit):
        for key in self.variables.keys():
            if self.variables[key].get() is not "":
                self.variables[key].set(convert_unit(self.ureg,prevvar=self.variables[key],\
                prevunit=self.startUnit,newunit=unit))

        self.startUnit.set(unit)

class InverseUnitValueController:
    def __init__(self,start=None,boundvar=None):
        self.ureg = pint.UnitRegistry()
        self.variables = {}
        for entry in boundvar:
            self.variables[entry[0]] = entry[1]

        self.startUnit = tk.StringVar()
        self.startUnit.set(start.get())

    def updateUnit(self,unit):
        temp1 = tk.StringVar()
        temp2 = tk.StringVar()
        for key in self.variables.keys():
            if self.variables[key].get() is not "":
                temp1.set(str(1/float(self.variables[key].get())))
                temp2.set(convert_unit(self.ureg,prevvar=temp1,\
                prevunit=self.startUnit,newunit=unit))
                self.variables[key].set(str(1/float(temp2.get())))

        self.startUnit.set(unit)

class SinglePattern:
    def __init__(self):
        super(SinglePattern, self).__init__()
        self.__defineVars__()

    def __defineVars__(self):
        self.varDict = dict(
            radius         = tk.StringVar(),\
            separation     = tk.StringVar(),\
            density        = tk.StringVar())

    def getVar(self,var):
        return self.varDict[var]

    def getParams(self):
        return self.varDict

    def setParams(self,key,value):
        self.varDict[key].set(value)

class SinglePrintController(WidgetVarIntegration):
    def __init__(self,update,patternDefaults=None):
        super(SinglePrintController,self).__init__()
        self.__defineVars__(update)

    def __defineVars__(self,update):
        self.update = update
        self.singlePattern = SinglePattern()
        self.varDict = dict(
            printWidth  = tk.StringVar(),\
            circleUnit  = tk.StringVar(),\
            densityUnit = tk.StringVar(),\
            printHeight = tk.StringVar(),\
            printUnit   = tk.StringVar(),\
            printType      = tk.BooleanVar())

    def setDefaults(self,defaultDict):
        dictSet(defaultDict["document"],self.varDict)
        dictSet(defaultDict["pattern1"],self.singlePattern.getParams())

    def getPatternDict(self):
        return self.singlePattern.getParams()

    def getDocumentDict(self):
        return self.varDict

    def getPatternV(self,varName):
        return self.singlePattern.getVar(varName)

    def getDocumentV(self,varName):
        return self.varDict[varName]

    def getPatternKV(self,varName):
        return [varName,self.singlePattern.getVar(varName)]

    def getDocumentKV(self,varName):
        return [varName,self.varDict[varName]]

class PatternController(WidgetVarIntegration):
    def __init__(self,changeFrame):
        super(PatternController,self).__init__()
        self.__defineVars__(changeFrame)

    def __defineVars__(self,changeFrame):
        self.changeFrame = changeFrame
        self.varDict = dict(patternFrameType  = tk.BooleanVar())

    def setDefaults(self,defaultDict):
        dictSet(defaultDict["pType"],self.varDict)

    def getV(self,varName):
        return self.varDict[varName]

    def getKV(self,varName):
        return [varName,self.varDict[varName]]

    def updateFrame(self):
        self.changeFrame()

class MultiPrintController(WidgetVarIntegration):
    def __init__(self,update):
        super(MultiPrintController,self).__init__()
        self.__defineVars__(update)

    def __defineVars__(self,update):
        self.update=update
        self.varDict = dict(
            documentWidth= tk.StringVar(),\
            documentHeight=tk.StringVar(),\
            documentUnit= tk.StringVar(),\
            printWidth  = tk.StringVar(),\
            printHeight = tk.StringVar(),\
            printUnit   = tk.StringVar(),\
            printMargin = tk.StringVar(),\
            printType   = tk.BooleanVar(),\
            circleUnit  = tk.StringVar(),\
            densityUnit = tk.StringVar(),\
            densitySelect = tk.BooleanVar(),\
            radiusSelect = tk.BooleanVar(),\
            separationSelect = tk.BooleanVar())

        self.checkList = []
        self.possibleChecks = ("densitySelect","radiusSelect","separationSelect")
        self.pattern1 = SinglePattern()
        self.pattern2 = SinglePattern()

    def getIndependentVariables(self):
        return tuple(self.checkList)

    def checkButtonCall(self,param):
        value = self.varDict[param].get()
        if value:
            self.checkList.append(param)
            if len(self.checkList) == 2:
                self.updatePattern()

            elif len(self.checkList) > 2:
                param0 = self.checkList.pop(0)
                self.varDict[param0].set(False)
                self.updatePattern()

        else:
            self.checkList.remove(param)

    def updatePattern(self):
        for key in self.possibleChecks:
            if key not in self.checkList:
                self.pattern2.setParams(key[:-6],"")

        self.update()

    def getDocumentDict(self):
        return self.varDict

    def getPatternDict(self,x=1):
        if x==1:
            return self.pattern1.getParams()
        else:
            return self.pattern2.getParams()

    def setDefaults(self,defaultDict):
        dictSet(defaultDict["document"],self.varDict)
        dictSet(defaultDict["pattern1"],self.pattern1.getParams())
        dictSet(defaultDict["pattern2"],self.pattern2.getParams())

    def getPatternV(self,x,key):
        if x==1:
            return self.pattern1.getVar(key)
        else:
            return self.pattern2.getVar(key)

    def getDocumentV(self,varName):
        return self.varDict[varName]

    def getDocumentKV(self,varName):
        return [varName,self.varDict[varName]]

    def getPatternKV(self,x,key):
        if x==1:
            return [key+str(x),self.pattern1.getVar(key)]
        else:
            return [key+str(x),self.pattern2.getVar(key)]

class AnalysisController:
    def __init__(self):
        self.__defineVars__()

    def __defineVars__(self):
        self.varDict = dict(\
            numericalOpacity    = tk.StringVar(),\
            theoreticalOpacity  = tk.StringVar(),\
            empiricalOpacity    = tk.StringVar())

    def getTkVar(self,key):
        return self.varDict[key]

    def setAnalysisString(self,analysis):
        self.varDict["theoreticalOpacity"].set(analysis[0])
        self.varDict["numericalOpacity"].set(analysis[1])

class InputController:
    def __init__(self):
        super(InputController, self).__init__()
        self.__defineVars__()

    def __defineVars__(self):
        self.varDict = dict(inputType= tk.StringVar(),\
                            inputImage= None)
        self.canvas = None
        self.file_opt = dict(defaultextension='.png',\
                             filetypes= [('png files', '.png')],\
                             message="Select a Source .png Image")

    def getImage(self):
        if self.varDict["inputType"].get()== "black":
            return None
        else:
            return self.varDict["inputImage"].copy()

    def getValue(self,key):
        return self.varDict[key]

    def setDefaults(self,defaultDict):
        dictSet(defaultDict["indef"],self.varDict)

    def radioUpdate(self):
        self.canvas.delete("all")
        if self.getValue("inputType").get() == "black":
            self.rectangleMethod()
        else:
            if self.getValue("inputImage") is None:
                self.loadImage()
            img = self.getValue("inputImage").copy()
            self.imageMethod(img)

    def createCanvas(self,frame,canvassParams,canvassMethods):
        self.imageMethod = canvassMethods["imageMethod"]
        self.rectangleMethod = canvassMethods["rectangleMethod"]
        self.canvas = tk.Canvas(frame,**canvassParams)
        return self.canvas

    def loadImage(self):
        img = PIL.Image.open(dialog.askopenfilename(**self.file_opt))
        img = img.convert("RGBA")
        self.varDict["inputImage"] = img.copy()

class SideController:
    def __init__(self, modelControl):
        self.__defineVars__(modelControl)

    def __defineVars__(self,modelControl):
        self.modelControl = modelControl
        self.changeFrame  = None
        self.defaults = dict(pType   = dict(patternFrameType  = True),\
                            indef    = dict(inputType="black"),\
                            pattern1 = dict(radius='0.1',separation='0.3',density='500'),\
                            pattern2 = dict(radius='0.5',separation='1.5',density='600'),\
                            document = dict(documentWidth="8.5",documentHeight="11",documentUnit="in",\
                                            printWidth="3",printHeight="3",printMargin="0.1",printUnit="cm",\
                                            printType=True,circleUnit="mm",densityUnit="cm"))

        self.controllers = dict(singlePrintControl=SinglePrintController(self.updateUnitCell),\
                               multiPrintControl=MultiPrintController(self.updateUnitCell),\
                               analysisControl=AnalysisController(),\
                               inputControl=InputController(),\
                               patternControl=PatternController(self.updateFrame))

        self.__setControllerDefaults__(self.controllers["patternControl"],self.defaults)
        self.__setControllerDefaults__(self.controllers["inputControl"],self.defaults)
        self.__setControllerDefaults__(self.controllers["multiPrintControl"],self.defaults)
        self.__setControllerDefaults__(self.controllers["singlePrintControl"],self.defaults)

    def __setControllerDefaults__(self,controller,defaults):
        controller.setDefaults(defaults)

    def getController(self,controller):
        return self.controllers.get(controller)

    def getImage(self):
        if self.controllers["inputControl"].getValue("InputType").get()==2:
            return self.controllers["inputControl"].getValue("InputImage")
        else:
            return None

    def getIndependentVariables(self):
        return self.getController("multiPrintControl").getIndependentVariables()

    def getPattern(self,x=1):
        if self.getFrameType():
            return self.getController("singlePrintControl").getPatternDict()
        else:
            if x==1:
                return self.getController("multiPrintControl").getPatternDict()
            else:
                return self.getController("multiPrintControl").getPatternDict(2)

    def getDocument(self):
        if self.getFrameType():
            return self.getController("singlePrintControl").getDocumentDict()
        else:
            return self.getController("multiPrintControl").getDocumentDict()

    def getImage(self):
        return self.getController("inputControl").getImage()

    def getFrameType(self):
        return self.getController("patternControl").getV("patternFrameType").get()

    def updateUnitCell(self):
        self.modelControl.updateUnitCell()

    def updateFrame(self):
        self.changeFrame(self.getController("patternControl").getV("patternFrameType").get())
        self.updateUnitCell()

    def setAnalysis(self,stringList):
        self.getController("analysisControl").setAnalysisString(stringList)

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
        if img is not None:
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
