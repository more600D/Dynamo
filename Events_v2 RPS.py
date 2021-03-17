# -*- coding: utf-8 -*-
import clr
clr.AddReference("RevitAPI")
from Autodesk.Revit.DB import IUpdater, UpdaterId, ChangePriority, UpdaterRegistry
from Autodesk.Revit.DB.Events import DocumentChangedEventArgs
clr.AddReference('RevitAPIUI')
from Autodesk.Revit.UI import TaskDialog
from Autodesk.Revit.UI.Selection import ObjectType, Selection
from Autodesk.Revit.UI.Events import DialogBoxData

doc = __revit__.ActiveUIDocument.Document
uiapp = __revit__
app = uiapp.Application


def get_deleted_elements(sender, args):
    # for d in args.GetDeletedElementIds():
    print('---------------')
    for d in args.GetModifiedElementIds():
        print(doc.GetElement(d).Name)
    # print([doc.GetElement(d) for d in args.GetModifiedElementIds()])


app.DocumentChanged += get_deleted_elements
