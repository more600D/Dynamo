import clr
clr.AddReference("RevitAPI")
from Autodesk.Revit.DB import FilteredElementCollector, BasePoint, CurveArray, BuiltInCategory
clr.AddReference("RevitServices")
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager
clr.AddReference("RevitNodes")
import Revit.Elements


doc = DocumentManager.Instance.CurrentDBDocument
uiapp = DocumentManager.Instance.CurrentUIApplication
app = uiapp.Application

floorModelCurves = UnwrapElement(IN[0])
openingModelCurves = UnwrapElement(IN[1])

elems = FilteredElementCollector(doc).OfClass(${0})().ToElements()


curveArray = CurveArray()
for modelCurve in floorModelCurves:
    curve = modelCurve.Location.Curve
    curveArray.Append(curve)
curveArray2 = CurveArray()
for modelCurve in openingModelCurves:
    curve = modelCurve.Location.Curve
    curveArray2.Append(curve)

TransactionManager.Instance.EnsureInTransaction(doc)
newFloor = doc.Create.NewFloor(curveArray, False)
doc.Regenerate()
opening = doc.Create.NewOpening(newFloor, curveArray2, True)

TransactionManager.Instance.TransactionTaskDone()



OUT = dir(Revit.Elements)
