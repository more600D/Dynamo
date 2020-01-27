# -*- coding: utf-8 -*-
import clr
clr.AddReference("RevitAPI")
from Autodesk.Revit.DB import FilteredElementCollector, BuiltInCategory, ParameterType
from itertools import groupby
clr.AddReference("RevitServices")
from RevitServices.Persistence import DocumentManager
# from RevitServices.Transactions import TransactionManager


def location_Rooms(rooms):
    mylist = []
    for r in rooms:
        if r.Location:
            mylist.append(r)
    return mylist


def group_by_key(elems, keyfunc):
    items = []
    uniqueKeys = []
    for key, group in groupby(elems, key=keyfunc):
        item = []
        for g in group:
            item.append(g)
        items.append(item)
        uniqueKeys.append(key)
    return items, uniqueKeys


def get_value_by_name(items, paramName):
    value = []
    for item in items:
        para = item.LookupParameter(paramName)
        if para and para.Definition.ParameterType == ParameterType.Text:
            if para.AsString() is None:
                value.append(0)
            else:
                value.append(int(para.AsString()))
        else:
            value.append(para.AsDouble())
    return value


doc = DocumentManager.Instance.CurrentDBDocument

el = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Rooms)

rooms_group_list = group_by_key(location_Rooms(el), lambda e: e.Level.Name)[0]

OUT = [get_value_by_name(g, 'Отделка пола') for g in rooms_group_list]
