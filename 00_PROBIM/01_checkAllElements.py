# -*- coding: utf-8 -*-
import clr
clr.AddReference("RevitAPI")
clr.AddReference("RevitServices")
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager
doc = DocumentManager.Instance.CurrentDBDocument


def get_all_elements_from_document(doc):
    from Autodesk.Revit.DB import FilteredElementCollector, Options
    all_elements = FilteredElementCollector(doc).WhereElementIsNotElementType().ToElements()
    elems = []
    for elem in all_elements:
        geo = elem.get_Geometry(Options())
        bb = elem.get_BoundingBox(None)
        if bb and geo:
            cat = elem.Category.Name
            if cat != "Cameras":
                elems.append(elem)
    return elems


OUT = get_all_elements_from_document(doc)
