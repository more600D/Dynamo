import System
import clr
clr.AddReference("RevitAPI")
from Autodesk.Revit.DB import FilteredElementCollector, BuiltInCategory, BuiltInParameter
clr.AddReference("RevitServices")
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager


doc = DocumentManager.Instance.CurrentDBDocument
uiapp = DocumentManager.Instance.CurrentUIApplication
app = uiapp.Application

lev = UnwrapElement(IN[0])  # noqa
guid = System.Guid('066eab6d-c348-4093-b0ca-1dfe7e78cb6e')

rooms = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Rooms).ToElements()
roomAtLevel = []
roomName = []

TransactionManager.Instance.EnsureInTransaction(doc)
for r in rooms:
    if r.LevelId == lev.Id:
        param_name = r.get_Parameter(BuiltInParameter.ROOM_NAME)
        param_koef = r.get_Parameter(guid)
        if param_koef:
            name = param_name.AsString()
            if name == 'Балкон':
                param_koef.Set(0.3)
            elif name == 'Лоджия':
                param_koef.Set(0.5)
            else:
                param_koef.Set(1.0)

        roomName.append(name)
        roomAtLevel.append(r.LevelId)
TransactionManager.Instance.TransactionTaskDone()

OUT = rooms
