import clr
clr.AddReference("RevitAPI")
from Autodesk.Revit.DB import FilteredElementCollector, FamilyInstance, BuiltInCategory, BuiltInParameter
clr.AddReference("RevitServices")
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager


doc = DocumentManager.Instance.CurrentDBDocument
uiapp = DocumentManager.Instance.CurrentUIApplication
app = uiapp.Application


def GetHostLevel(col, param_name):

    items = []
    TransactionManager.Instance.EnsureInTransaction(doc)

    for item in col:
        host = item.Host
        win_level = item.get_Parameter(BuiltInParameter.FAMILY_LEVEL_PARAM).AsElementId()
        host_level = host.get_Parameter(BuiltInParameter.WALL_BASE_CONSTRAINT).AsElementId()
        if doc.GetElement(win_level).Id != doc.GetElement(host_level).Id:
            param = item.LookupParameter(param_name)
            if param:
                param.Set('Разные уровни')
                items.append(item)
    return items

    TransactionManager.Instance.TransactionTaskDone()


win_col = FilteredElementCollector(doc).OfClass(FamilyInstance).OfCategory(BuiltInCategory.OST_Windows).ToElements()
drs_col = FilteredElementCollector(doc).OfClass(FamilyInstance).OfCategory(BuiltInCategory.OST_Doors).ToElements()

result = []
result.append(GetHostLevel(win_col, IN[1])) # noqa
result.append(GetHostLevel(drs_col, IN[1])) # noqa

OUT = result
