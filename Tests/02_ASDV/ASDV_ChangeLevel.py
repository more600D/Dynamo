# -*- coding: utf-8 -*-
import clr
clr.AddReference("RevitAPI")
from Autodesk.Revit.DB import FilteredElementCollector, Level, ElementLevelFilter, Element

clr.AddReference("RevitServices")
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager


doc = DocumentManager.Instance.CurrentDBDocument
uiapp = DocumentManager.Instance.CurrentUIApplication
app = uiapp.Application

def FindLevel(lev, name):
    for l in lev:
        if l.Name == name:
            return l.Id

col_levels = FilteredElementCollector(doc).OfClass(Level).ToElements()
elem_filter = ElementLevelFilter(FindLevel(col_levels, "Уровень 2"))

cats = doc.Settings.Categories

elems = []

for c in cats:
    collector = FilteredElementCollector(doc).OfCategory(c.Id).WherePasses(elem_filter).WhereElementIsNotElementType().ToElements()

elems.append(collector)

OUT =  elems
