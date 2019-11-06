import clr
clr.AddReference('RevitAPI')
from Autodesk.Revit.DB import FilteredElementCollector, Wall
clr.AddReference('RevitServices')
from RevitServices.Persistence import DocumentManager
clr.AddReference('RevitNodes')
from Revit.GeometryConversion import RevitToProtoCurve


doc = DocumentManager.Instance.CurrentDBDocument
el = FilteredElementCollector(doc).OfClass(Wall)

OUT = [RevitToProtoCurve.ToProtoType(i.Location.Curve) for i in el]
