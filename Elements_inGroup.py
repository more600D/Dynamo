import clr
clr.AddReference("RevitAPI")
from Autodesk.Revit.DB import FilteredElementCollector, Group
clr.AddReference("RevitServices")
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager


doc = DocumentManager.Instance.CurrentDBDocument
uiapp = DocumentManager.Instance.CurrentUIApplication
app = uiapp.Application

el = FilteredElementCollector(doc).OfClass(Group).ToElements()

TransactionManager.Instance.EnsureInTransaction(doc)
tr_list = []
for e in el:
    group = []
    if 'TR_' in e.Name:
        for i in e.GetMemberIds():
            group.append(doc.GetElement(i))
        for g in group:
            g.LookupParameter('Комментарии').Set(str(len(group)))
    tr_list.append(group)
TransactionManager.Instance.TransactionTaskDone()

OUT = tr_list
