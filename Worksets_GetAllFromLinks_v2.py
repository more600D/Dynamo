# -*- coding: utf-8 -*-
import clr
clr.AddReference("RevitAPI")
from Autodesk.Revit.DB import FilteredElementCollector, RevitLinkInstance, FilteredWorksetCollector, WorksetKind

clr.AddReference("RevitServices")
from RevitServices.Persistence import DocumentManager


doc = DocumentManager.Instance.CurrentDBDocument
uiapp = DocumentManager.Instance.CurrentUIApplication
app = uiapp.Application


rvtLinks = FilteredElementCollector(doc).OfClass(RevitLinkInstance).ToElements()
rvtDocs = [d.GetLinkDocument() for d in rvtLinks]
rvtNames = [d.Title for d in rvtDocs]

listWorksetNames = []
for d in rvtDocs:
    file_item = []
    workset_doc = FilteredWorksetCollector(d).OfKind(WorksetKind.UserWorkset).ToWorksets()
    for w in workset_doc:
        file_item.append(w.Name)
    listWorksetNames.append(file_item)


OUT = rvtNames, listWorksetNames
