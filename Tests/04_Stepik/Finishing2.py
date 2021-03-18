import clr
clr.AddReference("RevitAPI")
from Autodesk.Revit.DB import FilteredElementCollector, BuiltInCategory, Outline, BoundingBoxIntersectsFilter, \
    FamilyInstance, ElementCategoryFilter, BuiltInParameter, LogicalAndFilter, UnitUtils, \
    SpatialElementBoundaryOptions, SpatialElementGeometryCalculator, DisplayUnitType, ElementId
clr.AddReference("RevitServices")
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager

doc = DocumentManager.Instance.CurrentDBDocument


def get_type_or_instance_parameter(elem, builtInParameter):
    param = elem.get_Parameter(builtInParameter)
    if param and param.AsDouble() != 0.0:
        value = param.AsDouble()
        if value:
            return value
    else:
        param = elem.Symbol.get_Parameter(builtInParameter)
        return param.AsDouble()


def get_square(elem):
    param1 = get_type_or_instance_parameter(elem, BuiltInParameter.FURNITURE_WIDTH)
    param2 = get_type_or_instance_parameter(elem, BuiltInParameter.FAMILY_HEIGHT_PARAM)
    param3 = get_type_or_instance_parameter(elem, BuiltInParameter.CASEWORK_HEIGHT)
    param4 = get_type_or_instance_parameter(elem, BuiltInParameter.CASEWORK_WIDTH)
    if param1 and param2:
        return param1 * param2
    elif param3 and param4:
        return param3 * param4


def check_elem_in_room(elem_id, room):
    elem = doc.GetElement(elem_id)
    phase = doc.Phases[1]
    if elem:
        from_room = elem.FromRoom[phase]
        to_room = elem.ToRoom[phase]
        if from_room and from_room.Number == room.Number:
            return elem
        elif to_room and to_room.Number == room.Number:
            return elem


def get_room_solid(rooms, name):
    for room in rooms:
        calc = SpatialElementGeometryCalculator(doc)
        calc_geometry = calc.CalculateSpatialElementGeometry(room)
        solid = calc_geometry.GetGeometry()
        sum_area = 0
        opening_area = []
        for face in solid.Faces:
            if face.GetType().Name == 'CylindricalFace' or face.FaceNormal.Z == 0:
                info = calc_geometry.GetBoundaryFaceInfo(face)
                opening_area.append(info)
            #     for i in info:
            #         elem = doc.GetElement(i.SpatialBoundaryElement.HostElementId)
            #         insert_elem_ids = elem.FindInserts(False, False, False, False)
            #         for elem_id in insert_elem_ids:
            #             opening = (check_elem_in_room(elem_id, room))
            #             if opening:
            #                 opening_area.append(get_square(opening))
            #         if elem.CurtainGrid is None:
            #             sum_area += face.Area
        # room_param = room.LookupParameter(name)
        # if room_param:
        #     try:
        #         room_param.Set(sum_area - sum(opening_area))
        #     except Exception:
        return opening_area


result = []
room_col = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Rooms).ToElements()

OUT = get_room_solid(room_col, '000'), len(list(room_col))
