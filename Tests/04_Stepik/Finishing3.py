# -*- coding: utf-8 -*-
import clr
clr.AddReference("RevitAPI")
from Autodesk.Revit.DB import FilteredElementCollector, BuiltInParameter, SpatialElementBoundaryOptions, StorageType, \
    UnitUtils, DisplayUnitType, BuiltInCategory
clr.AddReference("RevitServices")
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager


doc = DocumentManager.Instance.CurrentDBDocument
uiapp = DocumentManager.Instance.CurrentUIApplication
app = uiapp.Application


def get_type_or_instance_parameter_value(family_instance, builtInParameter):
    param_instance = family_instance.get_Parameter(builtInParameter)
    if param_instance:
        value_instance = param_instance.AsDouble()
        if not param_instance or value_instance == 0:
            param_type = family_instance.Symbol.get_Parameter(builtInParameter)
            return param_type.AsDouble()
        else:
            return value_instance


def get_square(family_instance):
    param1 = get_type_or_instance_parameter_value(family_instance, BuiltInParameter.CASEWORK_WIDTH)
    param2 = get_type_or_instance_parameter_value(family_instance, BuiltInParameter.CASEWORK_HEIGHT)
    if param1 and param2:
        value = param1 * param2
        return value
    else:
        return 0


def get_inserts_in_room(wall_list, room):
    inserts_in_room = []
    for wall in wall_list:
        phase = list(wall.Document.Phases)[-1]
        inserts = wall.FindInserts(False, False, False, False)
        if inserts:
            for i in inserts:
                element_in_room = wall.Document.GetElement(i)
                to_room = element_in_room.ToRoom[phase]
                from_room = element_in_room.FromRoom[phase]
                if to_room and to_room.Number == room.Number:
                    inserts_in_room.append(element_in_room)
                elif from_room and from_room.Number == room.Number:
                    inserts_in_room.append(element_in_room)
    return inserts_in_room


def get_segments_length(segment_list):
    elements = []
    ids = []
    all_length = 0
    for segments in segment_list:
        for segment in segments:
            elem = doc.GetElement(segment.ElementId)
            if hasattr(elem, 'CurtainGrid'):
                if not elem.CurtainGrid:
                    all_length += segment.GetCurve().Length
                    if elem.Id not in ids:
                        ids.append(elem.Id)
                        elements.append(elem)
    return elements, all_length


def set_value_by_param_name(elem, parameter_name, value):
    param = elem.LookupParameter(parameter_name)
    if param:
        if param.StorageType == StorageType.String:
            val = UnitUtils.ConvertFromInternalUnits(value, DisplayUnitType.DUT_SQUARE_METERS)
            param.Set(str(val))
        elif param.StorageType == StorageType.Double:
            param.Set(value)


def get_full_square_wall_from_room(room, param_name):
    report = 1
    room_height = room.get_Parameter(BuiltInParameter.ROOM_HEIGHT).AsDouble()
    room_segments = room.GetBoundarySegments(SpatialElementBoundaryOptions())
    perimenter = get_segments_length(room_segments)[1]
    full_wall_square = room_height * perimenter

    elements_in_room = get_segments_length(room_segments)[0]
    inserts = get_inserts_in_room(elements_in_room, room)
    inserts_square = 0
    for ins in inserts:
        inserts_square += get_square(ins)
        if get_square(ins) == 0:
            report = 0
    total_square = full_wall_square - inserts_square
    value = total_square * report
    set_value_by_param_name(room, param_name, value)  # noqa
    return value

sel_room = UnwrapElement(IN[2])  # noqa

room_col = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Rooms).ToElements()

TransactionManager.Instance.EnsureInTransaction(doc)
report = []
for room in room_col:
    name = room.get_Parameter(BuiltInParameter.ROOM_NAME).AsString()
    number = room.Number
    total = UnitUtils.ConvertFromInternalUnits(get_full_square_wall_from_room(room,IN[1]),  # noqa
                                               DisplayUnitType.DUT_SQUARE_METERS)
    report.append('{}-{} - {:.2f} м2'.format(number, name, total))

TransactionManager.Instance.TransactionTaskDone()

OUT = report
