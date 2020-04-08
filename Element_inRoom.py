import clr
clr.AddReference("RevitAPI")
from Autodesk.Revit.DB import ElementOnPhaseStatus
clr.AddReference("RevitServices")
from RevitServices.Persistence import DocumentManager

doc = DocumentManager.Instance.CurrentDBDocument

elem = UnwrapElement(IN[1])


def GetRoomElement(elem):
    phases = elem.Document.Phases
    if phases.Size != 0:
        _room = None
    for _phase in phases:
        if elem.GetPhaseStatus(_phase.Id) != ElementOnPhaseStatus.Future:
            _room = elem.get_Room(_phase)
            return _room
    return _room


OUT = GetRoomElement(elem), elem.Category.Name
