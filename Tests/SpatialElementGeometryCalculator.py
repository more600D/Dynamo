import clr
clr.AddReference("RevitAPI")
from Autodesk.Revit.DB import FilteredElementCollector, BuiltInCategory, SpatialElementGeometryCalculator, \
    BuiltInParameter

clr.AddReference("RevitServices")
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager

doc = DocumentManager.Instance.CurrentDBDocument

room_col = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Rooms).ToElements()
calculator = SpatialElementGeometryCalculator(doc)

TransactionManager.Instance.EnsureInTransaction(doc)

facelist = []
for room in room_col:
    room_num = room.get_Parameter(BuiltInParameter.ROOM_NUMBER).AsString()
    result = calculator.CalculateSpatialElementGeometry(room)
    room_solid = result.GetGeometry()
    elems = []
    for face in room_solid.Faces:
        subfaceList = result.GetBoundaryFaceInfo(face)
        for sub in subfaceList:
            elem = doc.GetElement(sub.SpatialBoundaryElement.HostElementId)
            elem.get_Parameter(BuiltInParameter.ALL_MODEL_INSTANCE_COMMENTS).Set(room_num)
            elems.append(elem)
    facelist.append(elems)

TransactionManager.Instance.TransactionTaskDone()

OUT = facelist, room_col
