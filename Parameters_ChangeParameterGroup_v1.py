# -*- coding: utf-8 -*-
import clr
import System
clr.AddReference('RevitAPI')
from Autodesk.Revit.DB import BuiltInParameterGroup, FilteredElementCollector, SharedParameterElement
clr.AddReference('RevitServices')
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager
doc = DocumentManager.Instance.CurrentDBDocument


def parse_to_builtInParameterGroup(item):
    parse_item = System.Enum.Parse(
        BuiltInParameterGroup, item
    )
    return parse_item


# Получение всех общих параметров в проекте
params = FilteredElementCollector(doc).OfClass(SharedParameterElement).ToElements()
need_params = IN[1] # noqa

filtered_params = []

# Фильтрация списка общих параметров
for np in need_params:
    for p in params:
        if p.Name == np:
            filtered_params.append(p)

param_groups = IN[2] # noqa

# Изменение значения группирования параметра
TransactionManager.Instance.EnsureInTransaction(doc)

if filtered_params:
    for i in range(len(filtered_params)):
        if hasattr(filtered_params[i], 'GetDefinition'):
            parse_pg = parse_to_builtInParameterGroup(param_groups[i])
            filtered_params[i].GetDefinition().ParameterGroup = parse_pg

TransactionManager.Instance.TransactionTaskDone()

# На выходе имена параметров
OUT = [f.Name for f in filtered_params]
