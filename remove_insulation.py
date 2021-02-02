import clr
clr.AddReference("RevitAPI")
from Autodesk.Revit.DB import FilteredElementCollector
from Autodesk.Revit.DB.Plumbing import PipeInsulation
clr.AddReference("RevitServices")
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager


doc = DocumentManager.Instance.CurrentDBDocument
uiapp = DocumentManager.Instance.CurrentUIApplication
app = uiapp.Application

pipe_iso_col = FilteredElementCollector(doc).OfClass(PipeInsulation).ToElements()

TransactionManager.Instance.EnsureInTransaction(doc)
deleted = []
for pipe_iso in pipe_iso_col:
    elem = doc.GetElement(pipe_iso.HostElementId)
    elem_category_name = elem.Category.Name
    if elem_category_name == 'Pipe Fittings' or elem_category_name == 'Pipe Accessories':
        deleted.append(elem)
        doc.Delete(pipe_iso.Id)

TransactionManager.Instance.TransactionTaskDone()

OUT = deleted
