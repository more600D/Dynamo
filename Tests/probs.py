# -*- coding: utf-8 -*-
import clr
from itertools import groupby
clr.AddReference("RevitAPI")
from Autodesk.Revit.DB import FilteredElementCollector, FamilyInstance, BuiltInCategory, ElementId
clr.AddReference("RevitServices")
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager
from System.Collections.Generic import List
clr.AddReference('RevitAPIUI')
from Autodesk.Revit.UI.Selection import ObjectType, Selection

doc = DocumentManager.Instance.CurrentDBDocument
uidoc = DocumentManager.Instance.CurrentUIApplication.ActiveUIDocument


def selElements(col):  # Выделение элементов из списка ElementId
    elementIdList = List[ElementId]()
    for i in col:
        elementIdList.Add(i.Id)
    uidoc.Selection.SetElementIds(elementIdList)


def group_by_key(elems, keyfunc):
    items = []
    keys = []
    for key, group in groupby(sorted(elems, key=keyfunc), key=keyfunc):
        items.append(list(group))
        keys.append(key)
    return items, keys


def level_name(x):
    return doc.GetElement(x.LevelId).Name


def function_name(x):
    fam_type = x.Symbol
    param = fam_type.LookupParameter("ADSK_Отверстие_Функция")
    if param:
        return param.AsString()


def form_type(x):
    if x.LookupParameter("ADSK_Отверстие_Глубина"):
        return "Ниша"
    elif x.LookupParameter("ADSK_Размер_Диаметр"):
        return "Круглое"
    else:
        return "Прямоугольное"


holes_col = FilteredElementCollector(doc).OfClass(FamilyInstance).\
    OfCategory(BuiltInCategory.OST_GenericModel).WhereElementIsNotElementType().ToElements()

final_list = []
for hole in holes_col:
    fam_name = hole.Symbol.Family.Name
    if "Отв_"in fam_name or "Ниша_" in fam_name:
        final_list.append(hole)

count = 1
group_by_level = group_by_key(final_list, lambda x: level_name(x))[0]

# group_by_func = []
# mylist = []
# for el_by_level in group_by_level:
#     list_by_level = group_by_key(el_by_level, lambda x: function_name(x))[0]
#     group_by_func.append(list_by_level)

level = []
for el_level in group_by_level:
    f_list = []
    list_circle = []
    list_nisha = []
    list_rec = []
    for el in el_level:
        if el.LookupParameter("ADSK_Размер_Диаметр"):
            list_circle.append(el)
        elif el.LookupParameter("ADSK_Отверстие_Глубина"):
            list_nisha.append(el)
        else:
            list_rec.append(el)
    f_list.append(sorted(list_circle, key=lambda x: x.LookupParameter("ADSK_Размер_Диаметр").AsDouble()))
    f_list.append(sorted(list_nisha, key=lambda x: x.LookupParameter("ADSK_Отверстие_Ширина").AsDouble()))
    f_list.append(sorted(list_rec, key=lambda x: x.LookupParameter("ADSK_Отверстие_Ширина").AsDouble()))
    level.append(f_list)
# el_p = uidoc.Selection.PickObject(ObjectType.Element, 'Выбрать элемент')
# el = doc.GetElement(el_p)

OUT = level
