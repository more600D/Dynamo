# -*- coding: utf-8 -*-

import clr
clr.AddReference("RevitAPI")
from Autodesk.Revit.DB import FilteredElementCollector, ElementWorksetFilter, Instance
clr.AddReference("RevitServices")
from RevitServices.Persistence import DocumentManager
doc = DocumentManager.Instance.CurrentDBDocument

active_worset = doc.GetWorksetTable().GetActiveWorksetId()
filter_worset = ElementWorksetFilter(active_worset)
workset_name = doc.GetWorksetTable().GetWorkset(active_worset).Name

elements = FilteredElementCollector(doc).OfClass(Instance).WherePasses(filter_worset).ToElements()

OUT = elements, workset_name
