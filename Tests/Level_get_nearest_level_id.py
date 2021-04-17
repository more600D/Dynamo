# -*- coding: utf-8 -*-
import clr
clr.AddReference("RevitAPI")
from Autodesk.Revit.DB import Level, XYZ

clr.AddReference("RevitServices")
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager


doc = DocumentManager.Instance.CurrentDBDocument
uiapp = DocumentManager.Instance.CurrentUIApplication
app = uiapp.Application


nearest_level_id = Level.GetNearestLevelId(doc, 5)

viewport = UnwrapElement(IN[1])  # noqa

TransactionManager.Instance.EnsureInTransaction(doc)
viewport.LabelOffset = XYZ(0, 0, 0)
TransactionManager.Instance.TransactionTaskDone()


OUT = viewport
