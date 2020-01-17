import clr
clr.AddReference("RevitAPI")
from Autodesk.Revit.DB import FilteredElementCollector, BuiltInCategory, FamilyInstance
clr.AddReference("RevitServices")
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager


doc = DocumentManager.Instance.CurrentDBDocument
uiapp = DocumentManager.Instance.CurrentUIApplication
app = uiapp.Application

param = IN[0]  # noqa

el = FilteredElementCollector(doc).OfClass(FamilyInstance).OfCategory(BuiltInCategory.OST_DetailComponents)

items = []
levels = []

TransactionManager.Instance.EnsureInTransaction(doc)
for e in el:
    lev = doc.GetElement(e.OwnerViewId)
    e.LookupParameter(param).Set(lev.Name)
    items.append(e)
    levels.append(lev)
TransactionManager.Instance.TransactionTaskDone()

OUT = items, levels
