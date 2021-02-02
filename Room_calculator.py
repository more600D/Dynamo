import clr
clr.AddReference("RevitAPI")
from Autodesk.Revit.DB import FilteredElementCollector, SpatialElement, BuiltInCategory, \
    SpatialElementGeometryCalculator, BuiltInParameter

clr.AddReference("RevitServices")
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager


doc = DocumentManager.Instance.CurrentDBDocument
uiapp = DocumentManager.Instance.CurrentUIApplication
app = uiapp.Application


def set_value_to_parameter(el, name, value):
    TransactionManager.Instance.EnsureInTransaction(doc)
    param = el.LookupParameter(name)
    if param:
        param.Set(value)
        return'Ok'
    TransactionManager.Instance.TransactionTaskDone()


col = FilteredElementCollector(doc).OfClass(SpatialElement).OfCategory(BuiltInCategory.OST_Rooms).ToElements()


elements_in_rooms = []
calculator = SpatialElementGeometryCalculator(doc)

for room in col:
    room_number = room.get_Parameter(BuiltInParameter.ROOM_NUMBER).AsString()
    room_elements = []
    cal_geometry = calculator.CalculateSpatialElementGeometry(room)
    solid = cal_geometry.GetGeometry()
    for face in solid.Faces:
        for sub in cal_geometry.GetBoundaryFaceInfo(face):
            el = doc.GetElement(sub.SpatialBoundaryElement.HostElementId)
            set_value_to_parameter(el, 'Комментарии', room_number)
            room_elements.append(el)
    elements_in_rooms.append(room_elements)

OUT = elements_in_rooms
