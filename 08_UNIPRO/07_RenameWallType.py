import clr
clr.AddReference("RevitAPI")
from Autodesk.Revit.DB import WallType, FilteredElementCollector, BuiltInParameter

clr.AddReference("RevitServices")
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager


doc = DocumentManager.Instance.CurrentDBDocument


def rename_walltype(walltype_name, new_name):
    result = 'Undone :('
    wall_types = FilteredElementCollector(doc).OfClass(WallType).ToElements()
    for wtype in wall_types:
        param = wtype.get_Parameter(BuiltInParameter.SYMBOL_NAME_PARAM)
        if param.AsString() == walltype_name:
            wtype.Name = new_name
            result = 'Done! :)'
    return result


TransactionManager.Instance.EnsureInTransaction(doc)
info = rename_walltype(IN[0], IN[1])
TransactionManager.Instance.TransactionTaskDone()

OUT = info
