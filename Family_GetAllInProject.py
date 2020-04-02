import clr
clr.AddReference("RevitAPI")
from Autodesk.Revit.DB import FilteredElementCollector, Family, ImportInstance
clr.AddReference("RevitServices")
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager


doc = DocumentManager.Instance.CurrentDBDocument
uiapp = DocumentManager.Instance.CurrentUIApplication
app = uiapp.Application

el = FilteredElementCollector(doc).OfClass(ImportInstance).ToElements()

TransactionManager.Instance.EnsureInTransaction(doc)
for e in el:
    doc.Delete(e.Id)
TransactionManager.Instance.TransactionTaskDone()

OUT = 0