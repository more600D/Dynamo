# -*- coding: utf-8 -*-
import clr
clr.AddReference("RevitAPI")
from Autodesk.Revit.DB import FilteredElementCollector, BuiltInCategory
from itertools import groupby
clr.AddReference("RevitServices")
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager


def location_Rooms(rooms):
    mylist = []
    for r in rooms:
        if r.Location is not None:
            mylist.append(r)
    return mylist


def group_by_key(elems, keyValue):
    items = []
    uniqueKeys = []
    for key, group in groupby(elems, key=keyValue):
        item = []
        for g in group:
            item.append(g)
        items.append(item)
        uniqueKeys.append(key)
    return items, uniqueKeys


doc = DocumentManager.Instance.CurrentDBDocument

el = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Rooms)

OUT = group_by_key(location_Rooms(el), lambda e: e.Level.Name)
