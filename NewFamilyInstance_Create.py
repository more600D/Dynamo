import clr
clr.AddReference('RevitAPI')
from Autodesk.Revit.DB import *

clr.AddReference("RevitNodes")
import Revit
clr.ImportExtensions(Revit.Elements)
clr.ImportExtensions(Revit.GeometryConversion)

clr.AddReference("RevitServices")
import RevitServices
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager

doc = DocumentManager.Instance.CurrentDBDocument

element = UnwrapElement(IN[1])
points = UnwrapElement(IN[2])
famtype = UnwrapElement(IN[3])
elementlist = []

view = doc.GetElement(element.OwnerViewId)

TransactionManager.Instance.EnsureInTransaction(doc)
if famtype.IsActive == False:
	famtype.Activate()
	doc.Regenerate()
for point in points:
	newobj = doc.Create.NewFamilyInstance(point.ToXyz(),famtype,view)
	elementlist.append(newobj.ToDSType(False))
TransactionManager.Instance.TransactionTaskDone()

OUT = elementlist
