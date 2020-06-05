import clr
clr.AddReference("RevitAPI")
from Autodesk.Revit.DB import FilteredElementCollector, RevitLinkInstance, BuiltInCategory, \
    Outline, BoundingBoxIntersectsFilter, BuiltInParameter, UnitUtils, DisplayUnitType

clr.AddReference("RevitServices")
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager

doc = DocumentManager.Instance.CurrentDBDocument

rvtlinks = FilteredElementCollector(doc).OfClass(RevitLinkInstance).ToElements()
linkdoc = []
for r in rvtlinks:
    linkdoc.append(r.GetLinkDocument())

lnkdoc = linkdoc[0]
transform = rvtlinks[0].GetTotalTransform()

rooms = FilteredElementCollector(lnkdoc).OfCategory(BuiltInCategory.OST_Rooms).ToElements()
fam_col = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Furniture). \
    WhereElementIsNotElementType().ToElements()

mlist = []
for room in rooms:
    llist = []
    room_box = room.get_BoundingBox(None)
    boxMin = transform.OfPoint(room_box.Min)
    boxMax = transform.OfPoint(room_box.Max)
    outline = Outline(boxMin, boxMax)
    bbfilter = BoundingBoxIntersectsFilter(outline)
    fam_ins = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Furniture).WherePasses(bbfilter).ToElements()
    llist.append(fam_ins)
    param = room.get_Parameter(BuiltInParameter.ROOM_AREA).AsDouble()
    llist.append(UnitUtils.ConvertFromInternalUnits(param, DisplayUnitType.DUT_SQUARE_METERS))
    mlist.append(llist)

TransactionManager.Instance.EnsureInTransaction(doc)

flist = []
for f in fam_col:
    room = lnkdoc.GetRoomAtPoint(f.Location.Point)
    flist.append(room)
    room_number = room.get_Parameter(BuiltInParameter.ROOM_NUMBER).AsString()
    param = f.get_Parameter(BuiltInParameter.ALL_MODEL_INSTANCE_COMMENTS)
    if param:
        param.Set("Номер помещения {}".format(room_number))

TransactionManager.Instance.TransactionTaskDone()


OUT = flist, fam_col
