import clr
clr.AddReference("RevitAPI")
from Autodesk.Revit.DB import FilteredElementCollector, UnitUtils, DisplayUnitType, BuiltInCategory
clr.AddReference("RevitServices")
from RevitServices.Persistence import DocumentManager

doc = DocumentManager.Instance.CurrentDBDocument


def filterBasePoint(items):
    for i in items:
        return i


el = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_SharedBasePoint).ToElements()

bp = filterBasePoint(el)
x = UnitUtils.ConvertFromInternalUnits(bp.Position.X, DisplayUnitType.DUT_MILLIMETERS)
y = UnitUtils.ConvertFromInternalUnits(bp.Position.Y, DisplayUnitType.DUT_MILLIMETERS)

OUT = x, y, bp
