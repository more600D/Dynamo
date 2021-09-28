import clr
clr.AddReference("RevitAPI")
from Autodesk.Revit.DB import ColorFillScheme, FilteredElementCollector, ElementClassFilter, ElementId, View, \
    BuiltInCategory, Category

clr.AddReference("RevitServices")
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager


doc = DocumentManager.Instance.CurrentDBDocument

view = doc.ActiveView
class_filter = ElementClassFilter(ColorFillScheme)
color_fill_scheme = view.GetColorFillSchemeId(ElementId(99859))

col = FilteredElementCollector(doc).OfClass(ColorFillScheme).ToElements()

cat = Category.GetCategory(doc, BuiltInCategory.OST_Rooms)
color_scheme_id = view.GetColorFillSchemeId(cat.Id)

elem = doc.GetElement(color_scheme_id)

# OUT = [doc.GetElement(c) for c in color_fill_scheme]
OUT = elem