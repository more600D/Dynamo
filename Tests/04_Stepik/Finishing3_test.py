import clr
clr.AddReference("RevitAPI")
from Autodesk.Revit.DB import FilteredElementCollector, FamilyInstance, BuiltInCategory, Wall, ElementId, \
    ElementOnPhaseStatus

clr.AddReference("RevitServices")
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager


doc = DocumentManager.Instance.CurrentDBDocument
uiapp = DocumentManager.Instance.CurrentUIApplication
app = uiapp.Application

# wall_list = FilteredElementCollector(doc).OfClass(Wall)
# inserts_in_room = []
# for wall in wall_list:
#     phase = list(wall.Document.Phases)[0]
#     inserts = wall.FindInserts(False, False, False, False)
#     if inserts:
#         for i in inserts:
#             element_in_wall = wall.Document.GetElement(i)
#             status = element_in_wall.GetPhaseStatus(phase.Id)
#             if status != ElementOnPhaseStatus.Demolished and status != ElementOnPhaseStatus.Future:
#                 to_room = element_in_wall.ToRoom[phase]
#                 from_room = element_in_wall.FromRoom[phase]
#                 inserts_in_room.append(element_in_wall)
#                 inserts_in_room.append(element_in_wall)

wall = doc.GetElement(ElementId(408080))
inserts_in_room = []
phase = list(wall.Document.Phases)[1]
inserts = wall.FindInserts(False, False, False, False)
if inserts:
    for i in inserts:
        element_in_wall = wall.Document.GetElement(i)
        status = element_in_wall.GetPhaseStatus(phase.Id)
        if status == ElementOnPhaseStatus.New or status == ElementOnPhaseStatus.Existing:
            to_room = element_in_wall.ToRoom[phase]
            from_room = element_in_wall.FromRoom[phase]
            inserts_in_room.append(to_room)
            # inserts_in_room.append(from_room)

# door = wall.Document.GetElement(inserts[0])
# status = door.GetPhaseStatus(phase.Id)
# to_room = None
# if status != ElementOnPhaseStatus.Demolished and status != ElementOnPhaseStatus.Future:
#     to_room = door.ToRoom[phase]


OUT = inserts_in_room
