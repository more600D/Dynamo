import clr
clr.AddReference("RevitAPI")
from Autodesk.Revit.DB import FilteredElementCollector, Outline, BoundingBoxIntersectsFilter, \
    Wall, JoinGeometryUtils, Floor

clr.AddReference("RevitServices")
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager

doc = DocumentManager.Instance.CurrentDBDocument


def get_intersects_walls(elem):
    bbox = elem.get_BoundingBox(None)
    if bbox:
        outline = Outline(bbox.Min, bbox.Max)
        bbfilter = BoundingBoxIntersectsFilter(outline)
        intersects = FilteredElementCollector(doc).OfClass(Wall).WherePasses(bbfilter).ToElements()
    return intersects


def get_instance_byname(name):
    elems = FilteredElementCollector(doc).OfClass(Floor).ToElements()
    mlist = []
    for i in elems:
        if name in i.Name:
            mlist.append(i)
    return mlist


name = IN[2]
floor_type_name = IN[1]
walls = []

TransactionManager.Instance.EnsureInTransaction(doc)

floors = get_instance_byname(floor_type_name)
result = []
for elem in floors:
    for i in get_intersects_walls(elem):
        if i.Name == name:
            walls.append(i)
            try:
                JoinGeometryUtils.JoinGeometry(doc, elem, i)
                result.append('OK')
            except Exception:
                result.append('NOT OK')

TransactionManager.Instance.TransactionTaskDone()

OUT = result
