import Pattern_Model as model

def single_pattern(pattern_type=pattern,params=params):
    if pattern_type is "cell":
        unit_cell = model.unit_cell(get_normalized_vars(params))
        return unit_cell.get_image()
    else:
        return model.createpng(get_normalized_vars(params))

def multi_pattern(startvars=start,endvars=end,divvars=div,globalvars=glob):
    #example of input dictionaries
    glob   =dict(height=("3","cm"),\
                 width=("3","cm"),\
                 separation=("0.01","cm"),\
                 radius=("0.01","cm"),\
                 px_cm=("300","cm"),\
                 input_file=None,\
                 is_positive=False)

    start  =dict(separation=("0.01","cm"),\
                 radius=("0.01","cm"))

    end    =dict(separation=("0.2","cm"),\
                 radius=("0.1","cm"))

    divvars=dict(separation=5,\
                 radius=10)
    #################################
    ## General shit

    pass

def anayze_unit_cell(params=params):
    unit_cell = model.unit_cell(get_normalized_vars(params))
    return (unit_cell.get_theoretical_opacity(),unit_cell.get_numerical_opacity())

def __get_normalized_vars__(params):
    return model.Image_vars(params)
