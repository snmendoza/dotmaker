import model.PatternModel as model
import pint

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
        unit.getImage()
        self.display.updateCanvass(unit.getImage(),"cell")

    def __makeMultiUnitCell(self):
        documentDict = self.params.getDocument()
        independentVars = self.params.getIndependentVariables()
        pattern1  = self.params.getPattern()
        pattern2  = self.params.getPattern(x=2)
        cellDicts = makeParameterSpaceDicts(document=documentDict,patterns=(pattern1,pattern2),\
                                        indepVars=independentVars)
        cellimg = model.createMultiPrintCell(cellDicts)
        self.display.updateCanvass(cellimg,"cell")

    def __updateSinglePrint(self):
        patternDict  = self.params.getPattern()
        documentDict = self.params.getDocument()
        combinedDict = normalizeSinglePattern(documentDict,patternDict)
        combinedDict["input_file"] = self.params.getImage()
        self.img = model.createSinglePrintPng(combinedDict)
        self.display.updateCanvass(self.img.copy(),"print")

    def __updateMultiPrint(self):
        patternDict  = self.params.getPattern()
        documentDict = self.params.getDocument()
        #combinedDict = normalizeMultiPattern(documentDict,patternDict)
        #combinedDict["input_file"] = self.params.getImage()
        #self.img = model.createSinglePrintPng(combinedDict)
        #self.display.updateCanvass(self.img.copy(),"print")

    def updatePrintView(self):
        frameType = self.params.getFrameType()
        if frameType:
            self.__updateSinglePrint()
        else:
            self.__updateMultiPrint()

    def setPrintAnalysis(self):
        pass

    def save(self):
        return self.img.copy()

def anayze_unit_cell(params):
    unit_cell = model.unit_cell(get_normalized_vars(params))
    return (unit_cell.get_theoretical_opacity(),unit_cell.get_numerical_opacity())

def normalizeDocument(indict):
    ureg = pint.UnitRegistry()

def makeParameterSpaceDicts(document=None,patterns=None,indepVars=None):
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
            height=int(round(__normalize(ureg,documentDict["printWidth"],documentDict["printUnit"])*px_cm_conversion,0)), \
            width=int(round(__normalize(ureg,documentDict["printHeight"],documentDict["printUnit"])*px_cm_conversion,0)), \
            separation=int(round(__normalize(ureg,patternDict["separation"],documentDict["circleUnit"])*px_cm_conversion,0)),\
            radius=int(round(__normalize(ureg,patternDict["radius"],documentDict["circleUnit"])*px_cm_conversion,0)),\
            is_positive=documentDict["printType"].get(),\
            input_file=None)
        return default

def __normalize(ureg,prev,prevUnit):
    return float(ureg(prev.get() + prevUnit.get()).to("cm").magnitude)
