import clr
clr.AddReference('RevitAPI')
from Autodesk.Revit.DB import FilteredElementCollector, SharedParameterElement
clr.AddReference('RevitServices')
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager

doc = DocumentManager.Instance.CurrentDBDocument


def DeleteParams(params, name):
    for p in params:
        if p.Name == name:
            doc.Delete(p.Id)


name_param = IN[0]

params = FilteredElementCollector(doc).OfClass(SharedParameterElement)

TransactionManager.Instance.EnsureInTransaction(doc)
DeleteParams(params, name_param)
TransactionManager.Instance.TransactionTaskDone()

OUT = 0
