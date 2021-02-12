# -*- coding: utf-8 -*-
import clr
clr.AddReference("RevitAPI")
from Autodesk.Revit.DB import FilteredElementCollector, SpatialElement, BuiltInCategory, \
    SpatialElementGeometryCalculator, BuiltInParameter, FootPrintRoof, Options

clr.AddReference("RevitServices")
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager


doc = DocumentManager.Instance.CurrentDBDocument


def set_value_to_parameter(el, name, value):
    TransactionManager.Instance.EnsureInTransaction(doc)
    param = el.LookupParameter(name)
    if param:
        param.Set(value)
        return'Ok'
    TransactionManager.Instance.TransactionTaskDone()


def set_value_at_point(collector, param_name):
    rooms = []
    for r in collector:
        solids = r.get_Geometry(Options())
        for solid in solids:
            point = solid.ComputeCentroid()
            room = doc.GetRoomAtPoint(point)
            if room:
                rooms.append(room)
                room_number = room.get_Parameter(BuiltInParameter.ROOM_NUMBER).AsString()
                set_value_to_parameter(r, param_name, room_number)
    return rooms


def calculate_elements_in_room(room_collector, param_name):
    elements_in_rooms = []
    calculator = SpatialElementGeometryCalculator(doc)
    bad_rooms = []
    for room in room_collector:
        room_number = room.get_Parameter(BuiltInParameter.ROOM_NUMBER).AsString()
        room_elements = []
        try:
            cal_geometry = calculator.CalculateSpatialElementGeometry(room)
            solid = cal_geometry.GetGeometry()
            for face in solid.Faces:
                for sub in cal_geometry.GetBoundaryFaceInfo(face):
                    el = doc.GetElement(sub.SpatialBoundaryElement.HostElementId)
                    set_value_to_parameter(el, param_name, room_number)
                    room_elements.append(el)
            elements_in_rooms.append(room_elements)
        except Exception:
            bad_rooms.append(room)
    return elements_in_rooms, bad_rooms


col_room = FilteredElementCollector(doc).OfClass(SpatialElement).OfCategory(BuiltInCategory.OST_Rooms).ToElements()
col_roof = FilteredElementCollector(doc).OfClass(FootPrintRoof).ToElements()

atpoint_rooms = set_value_at_point(col_roof, IN[1])  # noqa
elements_in_rooms = calculate_elements_in_room(col_room, IN[1])  # noqa

OUT = atpoint_rooms, elements_in_rooms[0], elements_in_rooms[1]
