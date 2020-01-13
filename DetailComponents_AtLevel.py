import clr
clr.AddReference("RevitAPI")
from Autodesk.Revit.DB import FilteredElementCollector, BuiltInCategory
clr.AddReference("RevitServices")
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager


doc = DocumentManager.Instance.CurrentDBDocument
uiapp = DocumentManager.Instance.CurrentUIApplication
app = uiapp.Application

param = IN[0]  # noqa
el = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_DetailComponents).WhereElementIsNotElementType()

items = []
levels = []

TransactionManager.Instance.EnsureInTransaction(doc)
for e in el:
    if e.GetType().ToString() == 'Autodesk.Revit.DB.FamilyInstance':
        lev = doc.GetElement(e.OwnerViewId)
        levelName = lev.Name
        e.LookupParameter(param).Set(levelName)
        items.append(e)
        levels.append(lev)
TransactionManager.Instance.TransactionTaskDone()

OUT = items, levels
