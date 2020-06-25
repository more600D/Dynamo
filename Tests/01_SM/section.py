import clr
clr.AddReference("RevitAPI")
from Autodesk.Revit.DB import FilteredElementCollector, ElementIntersectsSolidFilter, Options, FamilyInstance, \
    ElementIntersectsElementFilter, Ceiling
from Autodesk.Revit.DB.Mechanical import Duct

el = UnwrapElement(IN[0])

doc = el.Document
opt = Options()
solid = el.get_Geometry(opt)

el_filter = ElementIntersectsElementFilter(el)
# solid_filter = ElementIntersectsSolidFilter(solid)

cats = []
cats.append(Duct)
cats.append(FamilyInstance)
cats.append(Ceiling)

col = []
for c in cats:
    intersectingInstances = FilteredElementCollector(doc).OfClass(c). \
        WherePasses(el_filter)
    el_list = list(intersectingInstances)
    if el_list:
        col.append(el_list)

OUT = col
