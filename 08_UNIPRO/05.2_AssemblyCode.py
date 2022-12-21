# -*- coding: utf-8 -*-
import clr
clr.AddReference("RevitAPI")
from Autodesk.Revit.DB import FilteredElementCollector, BuiltInParameter, WallType
clr.AddReference("RevitServices")
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager


doc = DocumentManager.Instance.CurrentDBDocument


def erase_data(wall_types):
    for w_type in wall_types:
        param = w_type.get_Parameter(BuiltInParameter.UNIFORMAT_CODE)
        if param:
            param.Set('')


def is_needed_material(material, name):
    if material:
        if name.lower() in material.Name.lower():
            return True


def set_assembly_code(wall_types, mat_name, code, function='All'):
    count = 0
    for w_type in wall_types:
        com_str = w_type.GetCompoundStructure()
        if com_str:
            layers = com_str.GetLayers()
            for layer in layers:
                mat = doc.GetElement(layer.MaterialId)
                if mat:
                    if mat_name.lower() in mat.Name.lower():
                        type_name = w_type.get_Parameter(BuiltInParameter.SYMBOL_NAME_PARAM).AsString()
                        param = w_type.get_Parameter(BuiltInParameter.UNIFORMAT_CODE)
                        if function in type_name:
                            param.Set(code)
                            count += 1
                        elif function == 'All':
                            param.Set(code)
                            count += 1
    return 'set - {} times'.format(count)


wall_type_col = FilteredElementCollector(doc).OfClass(WallType).ToElements()

# data = {
#     'sample': 'test'
# }

# values = {
#     'КВ': data,
#     'VK': data
# }

TransactionManager.Instance.EnsureInTransaction(doc)

rest = set_assembly_code(wall_type_col, 'Пазогребневые блоки невлагостойкие', 'КС.СП.02.04.02', 'ТЕХ')

TransactionManager.Instance.TransactionTaskDone()

OUT = rest
