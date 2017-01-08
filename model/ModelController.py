import model.PatternModel as model
import pint

class ModelControl:
    def __init__(self,actionControl=None,paramControl=None,displayControl=None):
        self.action=actionControl
        self.params=paramControl
        self.display=displayControl
        self.img=None

    def updateUnitCell(self):
        patternDict  = self.params.getPattern()
        documentDict = self.params.getDocument()
        if len(patternDict) > 1:
            print("multi Print")
            pass
        else:
            combinedDict = normalizePattern(documentDict,patternDict[0])
            unit = model.UnitCell(combinedDict)
            unit.getImage()
            self.display.updateCanvass(unit.getImage(),"cell")

    def updatePrintView(self):
        patternDict  = self.params.getPattern()
        documentDict = self.params.getDocument()
        if len(patternDict) > 1:
            print("multi Print")
            pass
        else:
            combinedDict = normalizePattern(documentDict,patternDict[0])
            combinedDict["input_file"] = self.params.getImage()
            self.img = model.createSinglePrintPng(combinedDict)
            self.display.updateCanvass(self.img.copy(),"print")

    def getPrintAnalysis(self):
        pass

    def save(self):
        return self.img.copy()

def anayze_unit_cell(params):
    unit_cell = model.unit_cell(get_normalized_vars(params))
    return (unit_cell.get_theoretical_opacity(),unit_cell.get_numerical_opacity())

def normalizeDocument(indict):
    ureg = pint.UnitRegistry()

def normalizePattern(documentDict,patternDict):
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
