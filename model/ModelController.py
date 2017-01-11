import model.PatternModel as model
import pint
import tkinter as tk

class ModelControl:
    def __init__(self,actionControl=None,paramControl=None,displayControl=None):
        self.action=actionControl
        self.params=paramControl
        self.display=displayControl
        self.img=None

    def updateUnitCell(self):
        frameType = self.params.getFrameType()
        if frameType:
            self.__makeSingleUnitCell()
        else:
            independentParams = self.params.getIndependentVariables()
            if len(independentParams) > 1:
                self.__makeMultiUnitCell()

    def __makeSingleUnitCell(self):
        patternDict  = self.params.getPattern()
        documentDict = self.params.getDocument()
        combinedDict = normalizeSinglePattern(documentDict,patternDict)
        unit = model.UnitCell(combinedDict)
        t = unit.theoreticalOpacity
        n = unit.numericalOpacity
        analysisString = (str(round(t*100,1)) + "%",str(round(n*100,1)) + "%")
        self.params.setAnalysis(analysisString)
        unit.getImage()
        self.display.updateCanvass(unit.getImage(),"cell")

    def __makeMultiUnitCell(self):
        if len(self.params.getIndependentVariables()) > 1:
            documentDict = self.params.getDocument()
            independentVars = self.params.getIndependentVariables()
            pattern1  = self.params.getPattern()
            pattern2  = self.params.getPattern(x=2)
            cellDicts = makeParameterCellSpaceDicts(document=documentDict,patterns=(pattern1,pattern2),\
                                        indepVars=independentVars)
            cellimg = model.createMultiPrintCell(cellDicts)
            analysisString = (" Min: " + str(round(min(cellimg[1])*100,1)) + "%"+" Max: " + str(round(max(cellimg[1])*100,1)) + "%",\
                              " Min: " + str(round(min(cellimg[2])*100,1)) + "%"+" Max: " + str(round(max(cellimg[2])*100,1)) + "%")
            self.params.setAnalysis(analysisString)
            self.display.updateCanvass(cellimg[0],"cell")

    def __updateSinglePrint(self):
        patternDict  = self.params.getPattern()
        documentDict = self.params.getDocument()
        combinedDict = normalizeSinglePattern(documentDict,patternDict)
        combinedDict["input_file"] = self.params.getImage()
        self.img = model.createSinglePrintPng(combinedDict)
        self.display.updateCanvass(self.img.copy(),"print")

    def __updateMultiPrint(self):
        if len(self.params.getIndependentVariables()) > 1:
            parameters = dict(document = self.params.getDocument(),\
                independentVars = self.params.getIndependentVariables(),\
                pattern1  = self.params.getPattern(),\
                pattern2  = self.params.getPattern(x=2),\
                imageBase = self.params.getImage())
            printDicts = makeParameterPrintSpaceDicts(parameters)
            normalizedDocumentDict = normalizeDocument(parameters)
            self.img = model.createMultiPrintPng(normalizedDocumentDict,printDicts)
            self.display.updateCanvass(self.img.copy(),"print")

    def updatePrintView(self):
        frameType = self.params.getFrameType()
        if frameType:
            self.__updateSinglePrint()
        else:
            self.__updateMultiPrint()

    def setPrintAnalysis(self):
        pass

    def save(self):
        if self.img is not None:
            return self.img.copy()
        return None

def anayze_unit_cell(params):
    unit_cell = model.unit_cell(get_normalized_vars(params))
    return (unit_cell.get_theoretical_opacity(),unit_cell.get_numerical_opacity())

def makeParameterPrintSpaceDicts(param):
    possibleStaticVars = ("densitySelect","radiusSelect","separationSelect")
    for var in possibleStaticVars:
        if var not in param['independentVars']:
            staticVar = var
    indepVars = param['independentVars']
    documentValues = getDocumentValues(param)
    xysubdivisions = getXYSubDivisions(documentValues)
    xychanges = getXYChanges(param)
    dxychanges = (xychanges[0]/xysubdivisions[0],xychanges[1]/xysubdivisions[1])
    dicts = [[None for i in range(xysubdivisions[1])] for j in range(xysubdivisions[0])]
    for x in range(0,xysubdivisions[0]):
        for y in range(0,xysubdivisions[1]):
            tempDict=dict(radius=tk.StringVar(),separation=tk.StringVar(),density=tk.StringVar())
            tempDict[staticVar[:-6]].set(param["pattern1"][staticVar[:-6]].get())
            tempDict[indepVars[0][:-6]].set(str(float(param["pattern1"][indepVars[0][:-6]].get()) + dxychanges[0]*x))
            tempDict[indepVars[1][:-6]].set(str(float(param["pattern1"][indepVars[1][:-6]].get()) + dxychanges[1]*y))
            dicts[x][y]=normalizeSinglePattern(param["document"],tempDict)
            dicts[x][y]["input_file"] = param["imageBase"]
    return dicts

def getXYChanges(param):
    indepvars = param["independentVars"]
    one = param["pattern1"]
    two = param["pattern2"]

    dx = float(two[indepvars[0][:-6]].get()) - float(one[indepvars[0][:-6]].get())
    dy = float(two[indepvars[1][:-6]].get()) - float(one[indepvars[1][:-6]].get())

    return (dx,dy)

def getXYSubDivisions(params):
    yunit = params["printHeight"] + params["printMargin"]
    xunit = params["printWidth"]  + params["printMargin"]
    xdist = params["documentWidth"]  - params["printMargin"]
    ydist = params["documentHeight"] - params["printMargin"]

    return (int(ydist/yunit),int(xdist/xunit))

def getDocumentValues(params):
    documentDict=params['document']
    ureg = pint.UnitRegistry()
    documentValues=dict( \
        printHeight=__normalize(ureg,documentDict["printHeight"],documentDict["printUnit"]), \
        printWidth=__normalize(ureg,documentDict["printWidth"],documentDict["printUnit"]), \
        printMargin=__normalize(ureg,documentDict["printMargin"],documentDict["printUnit"]),\
        documentHeight=__normalize(ureg,documentDict["documentHeight"],documentDict["documentUnit"]),\
        documentWidth=__normalize(ureg,documentDict["documentWidth"],documentDict["documentUnit"]))
    return documentValues

def makeParameterCellSpaceDicts(document=None,patterns=None,indepVars=None):
    dicts = [[None,None],[None,None]]
    possibleStaticVars = ("densitySelect","radiusSelect","separationSelect")
    for var in possibleStaticVars:
        if var not in indepVars:
            staticVar = var
    for first in range(2):
        for second in range(2):
            tempDict=dict(radius="",separation="",density="")
            tempDict[staticVar[:-6]] = patterns[0][staticVar[:-6]]
            tempDict[indepVars[0][:-6]]=patterns[first][indepVars[0][:-6]]
            tempDict[indepVars[1][:-6]]=patterns[second][indepVars[1][:-6]]
            dicts[first][second]=normalizeSinglePattern(document,tempDict)

    return dicts

def normalizeSinglePattern(documentDict,patternDict):
        ureg = pint.UnitRegistry()
        px_cm_conversion = __normalize(ureg,patternDict["density"],documentDict["densityUnit"])
        default=dict( \
            height=int(round(__normalize(ureg,documentDict["printHeight"],documentDict["printUnit"])*px_cm_conversion,0)), \
            width=int(round(__normalize(ureg,documentDict["printWidth"],documentDict["printUnit"])*px_cm_conversion,0)), \
            separation=int(round(__normalize(ureg,patternDict["separation"],documentDict["circleUnit"])*px_cm_conversion,0)),\
            radius=int(round(__normalize(ureg,patternDict["radius"],documentDict["circleUnit"])*px_cm_conversion,0)),\
            is_positive=documentDict["printType"].get(),\
            input_file=None)
        return default

def __normalize(ureg,prev,prevUnit):
    return float(ureg(prev.get() + prevUnit.get()).to("cm").magnitude)

def normalizeDocument(parameters):
    ureg = pint.UnitRegistry()
    if 'density' not in parameters['independentVars']:
        density = parameters['pattern1']['density']
    else:
        density = parameters['pattern1']['density']
        density2 = parameters['pattern2']['density']
        if float(density2) > float(density):
            density = density2
    documentDict=parameters['document']
    px_cm_conversion = __normalize(ureg,density,documentDict["densityUnit"])
    default=dict( \
        documentHeight=int(round(__normalize(ureg,documentDict["documentHeight"],documentDict["documentUnit"])*px_cm_conversion,0)), \
        documentWidth=int(round(__normalize(ureg,documentDict["documentWidth"],documentDict["documentUnit"])*px_cm_conversion,0)), \
        printHeight=int(round(__normalize(ureg,documentDict["printHeight"],documentDict["printUnit"])*px_cm_conversion,0)),\
        printWidth=int(round(__normalize(ureg,documentDict["printWidth"],documentDict["printUnit"])*px_cm_conversion,0)),\
        printMargin=int(round(__normalize(ureg,documentDict["printMargin"],documentDict["printUnit"])*px_cm_conversion,0)))
    return default
