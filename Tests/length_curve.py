import clr
clr.AddReference("RevitAPI")
from Autodesk.Revit.DB import FilteredElementCollector, CurveElement, BuiltInCategory, UnitUtils, DisplayUnitType, \
    View, ViewType, GraphicsStyleType, Color
clr.AddReference("RevitServices")
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager


doc = DocumentManager.Instance.CurrentDBDocument
uiapp = DocumentManager.Instance.CurrentUIApplication
app = uiapp.Application

views = FilteredElementCollector(doc).OfClass(View)

line_length = 0
TransactionManager.Instance.EnsureInTransaction(doc)

for v in views:
    if v.ViewType == ViewType.FloorPlan:
        scale = v.Scale
        elems = FilteredElementCollector(doc, v.Id).OfClass(CurveElement)
        for e in elems:
            graphics_style_cat = e.LineStyle.GraphicsStyleCategory
            id_cat = graphics_style_cat.Id
            if BuiltInCategory(id_cat.IntegerValue) == BuiltInCategory.OST_ProfileFamilies:
                cat = graphics_style_cat
                line_length += e.GeometryCurve.Length

gs = cat.GetGraphicsStyle(GraphicsStyleType.Projection)
gsCat = gs.GraphicsStyleCategory
gsCat.LineColor = Color(IN[1].Red, IN[1].Green, IN[1].Blue)  # noqa
v.Scale = 1
v.Scale = scale

line_length = UnitUtils.ConvertFromInternalUnits(line_length, DisplayUnitType.DUT_MILLIMETERS)

TransactionManager.Instance.TransactionTaskDone()

OUT = cat.Name
