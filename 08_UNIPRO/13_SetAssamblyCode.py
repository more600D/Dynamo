# -*- coding: utf-8 -*-
import clr
clr.AddReference("RevitAPI")
from Autodesk.Revit.DB import FilteredElementCollector, WallType, FloorType, CeilingType
clr.AddReference("RevitServices")
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager
doc = DocumentManager.Instance.CurrentDBDocument
data = IN[0]
sheet_name = IN[1]


def get_all_types(document, elemType):
    return FilteredElementCollector(document).OfClass(elemType).ToElements()


def set_assembly_code(type_list, data):
    from Autodesk.Revit.DB import BuiltInParameter
    result = []
    for elem in type_list:
        name = elem.get_Parameter(BuiltInParameter.ALL_MODEL_TYPE_NAME).AsString()
        assembly_param = elem.get_Parameter(BuiltInParameter.UNIFORMAT_CODE)
        try:
            value = data[name]
            if value == 999:
                assembly_param.Set("999")
            else:
                assembly_param.Set(value)
            result.append("{} - DONE".format(name))
        except KeyError as e:
            result.append("{} - UNDONE".format(name))
    return result


TransactionManager.Instance.EnsureInTransaction(doc)
if sheet_name == "Стены":
    result = set_assembly_code(get_all_types(doc, WallType), data)
elif sheet_name == "Перекрытия":
    result = set_assembly_code(get_all_types(doc, FloorType), data)
elif sheet_name == "Потолок":
    result = set_assembly_code(get_all_types(doc, CeilingType), data)
TransactionManager.Instance.TransactionTaskDone()

OUT = result