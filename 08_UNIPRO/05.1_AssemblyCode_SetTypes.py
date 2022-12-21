# -*- coding: utf-8 -*-
import clr
clr.AddReference("RevitAPI")
from Autodesk.Revit.DB import FilteredElementCollector, Wall, BuiltInParameter
clr.AddReference("RevitServices")
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager

doc = DocumentManager.Instance.CurrentDBDocument


def erase_date(elems, param_name='СТСП_Тип помещения'):
    for elem in elems:
        param = elem.LookupParameter(param_name)
        if param:
            if param.AsString() != '':
                param.Set('')


def set_data(elems, name_type, value_type, param_name='СТСП_Тип помещения'):
    count = 0
    for elem in elems:
        param = elem.LookupParameter(param_name)
        if param:
            type_name = elem.WallType.get_Parameter(BuiltInParameter.SYMBOL_NAME_PARAM).AsString()
            if name_type in type_name:
                param.Set(value_type)
                count += 1
    return 'set to {} elements'.format(count)


wall_col = FilteredElementCollector(doc).OfClass(Wall).ToElements()

type_values = {
    'КП': 'Коммерческие помещения',
    'ТЕХ': 'Технические помещения',
    'ИТП': 'ИТП',
    'МОП': 'МОП',
    'ЛХ': 'Лифтовые холлы',
    'КВ': 'Квартиры'
}

TransactionManager.Instance.EnsureInTransaction(doc)
erase_date(wall_col)
data = {}
for key, value in type_values.items():
    data[key] = set_data(wall_col, key, value)
TransactionManager.Instance.TransactionTaskDone()

OUT = data, doc.Title
