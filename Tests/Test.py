import clr
clr.AddReference("RevitAPI")
from Autodesk.Revit.DB import FilteredElementCollector, Wall
clr.AddReference("RevitNodes")
import Revit
clr.ImportExtensions(Revit.Elements)
clr.ImportExtensions(Revit.GeometryConversion)
clr.AddReference("RevitServices")
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager


doc = DocumentManager.Instance.CurrentDBDocument
uiapp = DocumentManager.Instance.CurrentUIApplication
app = uiapp.Application

apiCurve = UnwrapElement(IN[1])
level = UnwrapElement(IN[2])
el = UnwrapElement()

TransactionManager.Instance.EnsureInTransaction(doc)

wall = Wall.Create(doc, apiCurve.Location.Curve, level.Id, False).ToDSType(False)

TransactionManager.Instance.TransactionTaskDone()

OUT = wall
