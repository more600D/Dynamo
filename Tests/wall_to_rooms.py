import clr
clr.AddReference("RevitAPI")
from Autodesk.Revit.DB import FilteredElementCollector, Wall, Outline, BoundingBoxIntersectsFilter, \
    BuiltInCategory

clr.AddReference("RevitServices")
from RevitServices.Persistence import DocumentManager


doc = DocumentManager.Instance.CurrentDBDocument


def get_rooms(wall):
    document = wall.Document
    wall_bb = wall.get_BoundingBox(None)
    outline = Outline(wall_bb.Min, wall_bb.Max)
    bbfilter = BoundingBoxIntersectsFilter(outline)
    rooms = FilteredElementCollector(document).OfCategory(BuiltInCategory.OST_Rooms).\
        WherePasses(bbfilter).ToElements()
    return rooms


# rooms = []
# wall_col = FilteredElementCollector(doc).OfClass(Wall).ToElements()
# for wall in wall_col:
#     result = get_rooms(wall)
#     if result:
#         rooms.append(result)
#     else:
#         rooms.append(['No rooms'])



# OUT = rooms

OUT = get_rooms(UnwrapElement(IN[1]))  # noqa
