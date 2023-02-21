# -*- coding: utf-8 -*-
import clr
clr.AddReference("RevitAPI")
from Autodesk.Revit.DB import FilteredElementCollector, WallType, FloorType, CeilingType, SlabEdgeType
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
        for key in data.keys():
            if key in name:
                value = data[key]
                if value == 999:
                    assembly_param.Set("999")
                else:
                    assembly_param.Set(value)
                info = 'DONE'
                break
            else:
                info = 'UNDONE'
        result.append("{} - {}".format(name, info))
    return result


TransactionManager.Instance.EnsureInTransaction(doc)
if sheet_name == "Стены":
    result = set_assembly_code(get_all_types(doc, WallType), data)
elif sheet_name == "Перекрытия":
    result = set_assembly_code(get_all_types(doc, FloorType), data)
elif sheet_name == "Потолок":
    result = set_assembly_code(get_all_types(doc, CeilingType), data)
elif sheet_name == "Ребра плит":
    result = set_assembly_code(get_all_types(doc, SlabEdgeType), data)
TransactionManager.Instance.TransactionTaskDone()

OUT = result
