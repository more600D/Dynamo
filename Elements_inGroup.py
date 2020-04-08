import clr
clr.AddReference("RevitAPI")
from Autodesk.Revit.DB import FilteredElementCollector, Group
clr.AddReference("RevitServices")
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager

doc = DocumentManager.Instance.CurrentDBDocument

el = FilteredElementCollector(doc).OfClass(Group).ToElements()

TransactionManager.Instance.EnsureInTransaction(doc)
tr_list = []
for e in el:
    if 'TR_' in e.Name:
        group = []
        for i in e.GetMemberIds():
            group.append(doc.GetElement(i))
        for g in group:
            param = g.LookupParameter(IN[1])
            if param:
                param.Set(str(len(group)))
        tr_list.append(group)
TransactionManager.Instance.TransactionTaskDone()

OUT = tr_list
