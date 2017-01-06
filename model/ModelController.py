import model.PatternModel as model
import pint

class ModelControl:
    def __init__(self,actionControl=None,paramControl=None,displayControl=None):
        self.action=actionControl
        self.params=paramControl
        self.display=displayControl
        self.img=None

    def updateUnitCell(self,printType):
        if printType:
            self.param = single_print_dict_normalize(self.params.getParams())
            self.param["input_file"] = self.params.getImage()
            cell = model.Unit_Cell(self.param)
            self.display.updateCanvass(cell.get_image(),"cell")
        else:
            pass

    def updatePrintView(self):
        if self.params.getParamType():
            self.img = model.createPng(self.param)
            self.display.updateCanvass(self.img,"print")

    def getPrintAnalysis(self):
        pass

    def save(self):
        return self.img.copy()

def anayze_unit_cell(params):
    unit_cell = model.unit_cell(get_normalized_vars(params))
    return (unit_cell.get_theoretical_opacity(),unit_cell.get_numerical_opacity())

def single_print_dict_normalize(indict):
        ureg = pint.UnitRegistry()
        px_cm_conversion = __normalize(ureg,indict,"density","densityUnit")
        default=dict( \
            height=int(round(__normalize(ureg,indict,"documentHeight","documentUnit")*px_cm_conversion,0)), \
            width=int(round(__normalize(ureg,indict,"documentWidth","documentUnit")*px_cm_conversion,0)), \
            separation=int(round(__normalize(ureg,indict,"separation","circleUnit")*px_cm_conversion,0)),\
            radius=int(round(__normalize(ureg,indict,"radius","circleUnit")*px_cm_conversion,0)),\
            is_positive=indict.get("printType").get(),\
            input_file=None)
        return default

def __normalize(ureg,d,key,ukey):
    return float(ureg(d[key].get() + d[ukey].get()).to("cm").magnitude)
