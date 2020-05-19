import clr
clr.AddReference("RevitAPI")
from Autodesk.Revit.DB import FilteredElementCollector, BuiltInCategory, \
    ElementCategoryFilter, LogicalOrFilter
clr.AddReference("RevitServices")
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager


doc = DocumentManager.Instance.CurrentDBDocument
uiapp = DocumentManager.Instance.CurrentUIApplication
app = uiapp.Application


door_cat = ElementCategoryFilter(BuiltInCategory.OST_Doors)
win_cat = ElementCategoryFilter(BuiltInCategory.OST_Windows)

room_col = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Rooms).ToElements()
elements_col = FilteredElementCollector(doc).WherePasses(LogicalOrFilter(door_cat, win_cat)). \
    WhereElementIsNotElementType().ToElements()

phase = doc.Phases[1]

doors = []
for room in room_col:
    doors_in_room = []
    for door in elements_col:
        if door.FromRoom[phase]:
            if door.FromRoom[phase].Id == room.Id:
                doors_in_room.append(door)
        if door.ToRoom[phase]:
            if door.ToRoom[phase].Id == room.Id:
                doors_in_room.append(door)
    doors.append(doors_in_room)

OUT = doors
