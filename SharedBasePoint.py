import clr
clr.AddReference("RevitAPI")
from Autodesk.Revit.DB import FilteredElementCollector, BasePoint, UnitUtils, DisplayUnitType, BuiltInCategory
clr.AddReference("RevitServices")
from RevitServices.Persistence import DocumentManager

doc = DocumentManager.Instance.CurrentDBDocument

el = FilteredElementCollector(doc).OfClass(BasePoint).OfCategory(BuiltInCategory.OST_SharedBasePoint).ToElements()

bp = list([i for i in el])[0]
x = UnitUtils.ConvertFromInternalUnits(bp.Position.X, DisplayUnitType.DUT_MILLIMETERS)
y = UnitUtils.ConvertFromInternalUnits(bp.Position.Y, DisplayUnitType.DUT_MILLIMETERS)

OUT = x, y, bp
