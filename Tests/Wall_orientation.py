import clr
clr.AddReference("RevitAPI")
from Autodesk.Revit.DB import FilteredElementCollector, Wall
clr.AddReference("RevitServices")
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager


doc = DocumentManager.Instance.CurrentDBDocument
uiapp = DocumentManager.Instance.CurrentUIApplication
app = uiapp.Application

col = FilteredElementCollector(doc).OfClass(Wall).ToElements()
curtain_wall = []
for c in col:
    if c.CurtainGrid:
        curtain_wall.append(c.Orientation)


OUT = curtain_wall
