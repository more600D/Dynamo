import clr
clr.AddReference("RevitAPI")
from Autodesk.Revit.DB import FilteredElementCollector, BuiltInCategory, Outline, BoundingBoxIntersectsFilter, \
    FamilyInstance, ElementCategoryFilter, BuiltInParameter, LogicalAndFilter, UnitUtils
clr.AddReference("RevitServices")
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager


def getTypeOrInstanceParameter(elem, builtInParameter):
    param = elem.get_Parameter(builtInParameter)
    if param:
        value = param.AsDouble()
        if value:
            return value
        else:
            param = elem.Symbol.get_Parameter(builtInParameter)
            return param.AsDouble()


def square(elem):
    param1 = getTypeOrInstanceParameter(elem, BuiltInParameter.FURNITURE_WIDTH)
    param2 = getTypeOrInstanceParameter(elem, BuiltInParameter.FAMILY_HEIGHT_PARAM)
    if param1 and param2:
        value = param1 * param2
        return value


doc = DocumentManager.Instance.CurrentDBDocument

door_cat = ElementCategoryFilter(BuiltInCategory.OST_Doors)
win_cat = ElementCategoryFilter(BuiltInCategory.OST_Windows)

room_col = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Rooms).ToElements()

elements = []
square_value = []

TransactionManager.Instance.EnsureInTransaction(doc)

for room in room_col:
    room_box = room.get_BoundingBox(None)
    param = room.LookupParameter('ПлощадьПроемов')
    if room_box:
        outline = Outline(room_box.Min, room_box.Max)
        bbfilter = BoundingBoxIntersectsFilter(outline)
        doors = FilteredElementCollector(doc).OfClass(FamilyInstance). \
            WherePasses(LogicalAndFilter(bbfilter, door_cat)).ToElements()
        windows = FilteredElementCollector(doc).OfClass(FamilyInstance). \
            WherePasses(LogicalAndFilter(bbfilter, win_cat)).ToElements()
        fam_in_room = []
        value = 0
        for door in doors:
            value += square(door)
            fam_in_room.append(door)
        for window in windows:
            if square(window):
                value += square(window)
            fam_in_room.append(window)
        param.Set(value)
    elements.append(fam_in_room)
    square_value.append(UnitUtils.ConvertFromInternalUnits(value, param.DisplayUnitType))


TransactionManager.Instance.TransactionTaskDone()

OUT = elements, square_value
