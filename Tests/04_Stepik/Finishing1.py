import clr
clr.AddReference("RevitAPI")
from Autodesk.Revit.DB import FilteredElementCollector, BuiltInCategory, Outline, BoundingBoxIntersectsFilter, \
    FamilyInstance, ElementCategoryFilter, BuiltInParameter, LogicalAndFilter, UnitUtils, \
    SpatialElementBoundaryOptions
clr.AddReference("RevitServices")
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager


def get_type_or_instance_parameter_value(elem, builtInParameter):
    param_instance = elem.get_Parameter(builtInParameter)
    value_instance = param_instance.AsDouble()
    if not param_instance or value_instance == 0:
        param_type = elem.Symbol.get_Parameter(builtInParameter)
        return param_type.AsDouble()
    else:
        return value_instance


def get_square(elem):
    param1 = get_type_or_instance_parameter_value(elem, BuiltInParameter.CASEWORK_WIDTH)
    param2 = get_type_or_instance_parameter_value(elem, BuiltInParameter.CASEWORK_HEIGHT)
    if param1 and param2:
        value = param1 * param2
        return value


doc = DocumentManager.Instance.CurrentDBDocument

door_cat = ElementCategoryFilter(BuiltInCategory.OST_Doors)
win_cat = ElementCategoryFilter(BuiltInCategory.OST_Windows)

room_col = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Rooms).ToElements()

elements = []
square_value = []

opt = SpatialElementBoundaryOptions()
TransactionManager.Instance.EnsureInTransaction(doc)

for room in room_col:
    room_height_param = room.get_Parameter(BuiltInParameter.ROOM_HEIGHT)
    segments_list = room.GetBoundarySegments(opt)
    all_length = 0
    elem_in_room = []
    for segments in segments_list:
        for segment in segments:
            element_segement = doc.GetElement(segment.ElementId)
            hasCurtainGrid = hasattr(element_segement, 'CurtainGrid')
            if hasCurtainGrid:
                if element_segement.CurtainGrid is None:
                    all_length += segment.GetCurve().Length
                else:
                    elem_in_room.append(element_segement)
            else:
                hasCurveElementType = hasattr(element_segement, 'CurveElementType')
                if not hasCurveElementType:
                    all_length += segment.GetCurve().Length
                else:
                    elem_in_room.append(element_segement)
    all_square = all_length * room_height_param.AsDouble()
    room_box = room.get_BoundingBox(None)
    param = room.LookupParameter('ПлощадьПроемов')
    if room_box:
        fff = []
        outline = Outline(room_box.Min, room_box.Max)
        bbfilter = BoundingBoxIntersectsFilter(outline)
        doors = FilteredElementCollector(doc).OfClass(FamilyInstance). \
            WherePasses(LogicalAndFilter(bbfilter, door_cat)).ToElements()
        windows = FilteredElementCollector(doc).OfClass(FamilyInstance). \
            WherePasses(LogicalAndFilter(bbfilter, win_cat)).ToElements()
        value = 0
        for door in doors:
            try:
                value += get_square(door)
                elem_in_room.append(door)
            except Exception:
                fff.append(door)
        for window in windows:
            if get_square(window):
                value += get_square(window)
            elem_in_room.append(window)
        finish_square = all_square - value
        # param.Set(finish_square)
    elements.append(elem_in_room)
    # square_value.append(UnitUtils.ConvertFromInternalUnits(finish_square, param.DisplayUnitType))


TransactionManager.Instance.TransactionTaskDone()

OUT = fff
