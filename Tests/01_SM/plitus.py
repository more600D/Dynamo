import clr
clr.AddReference("RevitAPI")
from Autodesk.Revit.DB import FilteredElementCollector, BuiltInCategory, SpatialElementBoundaryOptions

clr.AddReference("RevitServices")
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager


def get_elems_from_boundaries(room):
    doc = room.Document
    opt = SpatialElementBoundaryOptions()
    result = []
    inserts = []
    room_boundaries = room.GetBoundarySegments(opt)
    for list_items in room_boundaries:
        filter_list = []
        for item in list_items:
            elem = doc.GetElement(item.ElementId)
            if not hasattr(elem, 'CurveElementType'):
                if not hasattr(elem, 'CurtainGrid'):
                    filter_list.append(elem)
                elif elem.CurtainGrid is None:
                    filter_list.append(elem)
                    a = elem.GetType().Name
                    i = elem.FindInserts(False, False, False, False)
        result.append(filter_list)
    return i


doc = DocumentManager.Instance.CurrentDBDocument
uiapp = DocumentManager.Instance.CurrentUIApplication
app = uiapp.Application

col_room = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Rooms)

boundaries = []
err = []
opt = SpatialElementBoundaryOptions()

for c in col_room:
    if c.Location and c.Perimeter != 0:
        boundaries.append(get_elems_from_boundaries(c))


OUT = boundaries
