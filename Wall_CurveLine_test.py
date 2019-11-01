import clr
clr.AddReference('RevitApi')
from Autodesk.Revit.DB import FilteredElementCollector, Wall
clr.AddReference('RevitServices')
from RevitServices.Persistence import DocumentManager
clr.AddReference('RevitNodes')
from Revit.GeometryConversion import RevitToProtoCurve


doc = DocumentManager.Instance.CurrentDBDocument

items_walls = FilteredElementCollector(doc).OfClass(Wall)

wall_lines = [RevitToProtoCurve.ToProtoType(i.Location.Curve) for i in items_walls]

OUT = wall_lines
