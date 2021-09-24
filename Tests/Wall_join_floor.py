import clr
clr.AddReference("RevitAPI")
from Autodesk.Revit.DB import FilteredElementCollector, Wall, Outline, BoundingBoxIntersectsFilter, \
    Floor, JoinGeometryUtils, Transaction, FootPrintRoof
clr.AddReference("RevitServices")
from RevitServices.Persistence import DocumentManager

doc = DocumentManager.Instance.CurrentDBDocument


def join_elements(collection, wall):
    result = False
    for c in collection:
        if not JoinGeometryUtils.AreElementsJoined(doc, c, wall):
            try:
                JoinGeometryUtils.JoinGeometry(doc, c, wall)
                result = True
            except Exception:
                pass
    return result


wall_col = FilteredElementCollector(doc).OfClass(Wall)
with Transaction(doc, '_Join elements') as t:
    t.Start()
    for w in wall_col:
        bbox = w.get_BoundingBox(None)
        if bbox:
            outline = Outline(bbox.Min, bbox.Max)
            bbfilter = BoundingBoxIntersectsFilter(outline)
            floor_col = FilteredElementCollector(doc).OfClass(Floor).WherePasses(bbfilter).ToElements()
            roof_col = FilteredElementCollector(doc).OfClass(FootPrintRoof).WherePasses(bbfilter).ToElements()
            join_elements(floor_col, w)
            join_elements(roof_col, w)
    t.Commit()

OUT = error
