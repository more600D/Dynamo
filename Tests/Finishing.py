import clr
clr.AddReference("RevitAPI")
from Autodesk.Revit.DB import FilteredElementCollector, BuiltInCategory, \
    ElementCategoryFilter, LogicalOrFilter, BuiltInParameter, UnitUtils
clr.AddReference("RevitServices")
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager

doc = DocumentManager.Instance.CurrentDBDocument
uiapp = DocumentManager.Instance.CurrentUIApplication
app = uiapp.Application


def getTypeOrInstanceParameter(elem, builtInParameter):
    param = elem.get_Parameter(builtInParameter)
    if param:
        if param.AsDouble():
            return param.AsDouble()
    else:
        if elem.Symbol.get_Parameter(builtInParameter).AsDouble():
            return elem.Symbol.get_Parameter(builtInParameter).AsDouble()


error = []


def square(elem):
    global error
    values = []
    try:
        value = getTypeOrInstanceParameter(elem, BuiltInParameter.FURNITURE_WIDTH) * \
            getTypeOrInstanceParameter(elem, BuiltInParameter.FAMILY_HEIGHT_PARAM)
        values.append(value)
    except:
        error.append(elem)
    return values


door_cat = ElementCategoryFilter(BuiltInCategory.OST_Doors)
win_cat = ElementCategoryFilter(BuiltInCategory.OST_Windows)

room_col = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Rooms).ToElements()
elements_col = FilteredElementCollector(doc).WherePasses(LogicalOrFilter(door_cat, win_cat)). \
    WhereElementIsNotElementType().ToElements()

phase = doc.Phases[1]

elements = []
sum_square = []

TransactionManager.Instance.EnsureInTransaction(doc)

for room in room_col:
    # param = room.LookupParameter('ПлощадьПроемов')
    elements_in_room = []
    elem_square = []
    for elem in elements_col:
        if elem.FromRoom[phase]:
            if elem.FromRoom[phase].Id == room.Id:
                elements_in_room.append(elem)
                elem_square.append(square(elem))
        if elem.ToRoom[phase]:
            if elem.ToRoom[phase].Id == room.Id:
                elements_in_room.append(elem)
                elem_square.append(square(elem))
    elements.append(elements_in_room)
    sum_square.append(elem_square)

TransactionManager.Instance.TransactionTaskDone()

OUT = elements[0][0].get_Parameter(BuiltInParameter.FURNITURE_WIDTH)
