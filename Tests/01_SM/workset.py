import clr
clr.AddReference("RevitAPI")
from Autodesk.Revit.DB import FilteredElementCollector, FilteredWorksetCollector, BuiltInCategory, WorksetKind, \
    BuiltInParameter
clr.AddReference("RevitServices")
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager


doc = DocumentManager.Instance.CurrentDBDocument


def GetWorkSet(name):
    worksets = FilteredWorksetCollector(doc).OfKind(WorksetKind.UserWorkset).ToWorksets()
    for w in worksets:
        if w.Name == name:
            return w.Id.IntegerValue


def SetWorkSet(cat, name):
    elems = FilteredElementCollector(doc).OfCategory(cat). \
        WhereElementIsNotElementType().ToElements()

    TransactionManager.Instance.EnsureInTransaction(doc)

    for e in elems:
        param = e.get_Parameter(BuiltInParameter.ELEM_PARTITION_PARAM)
        if param:
            worksetId = GetWorkSet(name)
            if worksetId:
                param.Set(worksetId)
                msg = 'ОК'
            else:
                msg = 'Нет такого набора: {}'.format(name)
    return msg

    TransactionManager.Instance.TransactionTaskDone()


result = []
result.append(SetWorkSet(BuiltInCategory.OST_Doors, '01_Двери'))
result.append(SetWorkSet(BuiltInCategory.OST_Windows, '01_Окна'))
result.append(SetWorkSet(BuiltInCategory.OST_StairsRailing, '02_Лестницы'))
result.append(SetWorkSet(BuiltInCategory.OST_Stairs, '02_Лестницы'))
result.append(SetWorkSet(BuiltInCategory.OST_Grids, '00_ОсиУровни'))
result.append(SetWorkSet(BuiltInCategory.OST_Levels, '00_ОсиУровни'))

OUT = result
