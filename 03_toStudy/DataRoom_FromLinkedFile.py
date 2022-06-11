import clr
clr.AddReference("RevitAPI")
from Autodesk.Revit.DB import FilteredElementCollector, SpatialElement, BuiltInCategory, RevitLinkInstance, XYZ

clr.AddReference("RevitServices")
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager


doc = DocumentManager.Instance.CurrentDBDocument


def get_linked_file_byname(name):
    rvt_links = FilteredElementCollector(doc).OfClass(RevitLinkInstance).ToElements()
    if rvt_links:
        for i in rvt_links:
            if name in i.Name:
                return i

def get_rooms_from_document(doc):
    rooms = FilteredElementCollector(doc).OfClass(SpatialElement). \
        OfCategory(BuiltInCategory.OST_Rooms).ToElements()
    return rooms


def get_set_to_element(from_elem, to_elem, from_param_name, to_param_name):
    f_param = from_elem.LookupParameter(from_param_name)
    if f_param: value = f_param.AsString()
    to_param = to_elem.LookupParameter(to_param_name)
    if to_param: to_param.Set(value)


link_doc = get_linked_file_byname('СНомерами.rvt').GetLinkDocument()
current_rooms = get_rooms_from_document(doc)

TransactionManager.Instance.EnsureInTransaction(doc)

for room in current_rooms:
    link_room = link_doc.GetRoomAtPoint(room.Location.Point)
    get_set_to_element(link_room, room, 'Name', 'Name')
    get_set_to_element(link_room, room, 'Number', 'Number')

TransactionManager.Instance.TransactionTaskDone()

OUT = room