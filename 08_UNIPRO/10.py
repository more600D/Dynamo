import clr
clr.AddReference("RevitAPI")
from Autodesk.Revit.DB import Wall, BuiltInCategory, FamilyInstance
clr.AddReference("RevitServices")
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager


doc = DocumentManager.Instance.CurrentDBDocument
uiapp = DocumentManager.Instance.CurrentUIApplication
app = uiapp.Application


def set_data_to_parameter(document, elem, param_name, data):
    param = elem.LookupParameter(param_name)
    result = "Done!"
    if param:
        param.Set(data)
    else:
        elem_type = document.GetElement(elem.GetTypeId())
        elem_type_param = elem_type.LookupParameter(param_name)
        if elem_type_param:
            elem_type_param.Set(data)
        else:
            result = "There is no such parameter"
    return result


def set_data_to_element(document, class_type, t_name, param_name, data, category):
    from Autodesk.Revit.DB import FilteredElementCollector, BuiltInParameter
    elemes = FilteredElementCollector(document).OfClass(class_type).OfCategory(category).ToElements()
    result = 'Нет такого типа. :('
    info = []
    for elem in elemes:
        type_name = elem.get_Parameter(BuiltInParameter.ELEM_TYPE_PARAM).AsValueString()
        if t_name.lower() in type_name.lower():
            result = set_data_to_parameter(document, elem, param_name, data)
    info.append(result)
    return info



class_type = FamilyInstance
t_name = "1810x910mm"
param_name = "Comments"
data = "test"
cat = BuiltInCategory.OST_Windows

TransactionManager.Instance.EnsureInTransaction(doc)
result = set_data_to_element(doc, class_type, t_name, param_name, data, cat)
TransactionManager.Instance.TransactionTaskDone()

OUT = result