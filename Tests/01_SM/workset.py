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


def SetWorkSet_byCategory(cat, name):
    elems = FilteredElementCollector(doc).OfCategory(cat). \
        WhereElementIsNotElementType().ToElements()

    TransactionManager.Instance.EnsureInTransaction(doc)
    if elems:
        for e in elems:
            param = e.get_Parameter(BuiltInParameter.ELEM_PARTITION_PARAM)
            if param:
                worksetId = GetWorkSet(name)
                if worksetId:
                    try:
                        param.Set(worksetId)
                    except Exception:
                        pass
                    msg = 'ОК'
                else:
                    msg = 'Нет такого набора: {}'.format(name)
    else:
        msg = "Нет элементов категории {}".format(cat)
    return msg

    TransactionManager.Instance.TransactionTaskDone()


def SetWorkSet_byElement(elem, name):
    param = elem.get_Parameter(BuiltInParameter.ELEM_PARTITION_PARAM)
    if param:
        worksetId = GetWorkSet(name)
        if worksetId:
            param.Set(worksetId)
            msg = 'ОК'
        else:
            msg = 'Нет такого набора: {}'.format(name)
    return msg


cats = []
cats.append(BuiltInCategory.OST_Walls)
cats.append(BuiltInCategory.OST_Floors)

result = []

TransactionManager.Instance.EnsureInTransaction(doc)

for c in cats:
    elems = FilteredElementCollector(doc).OfCategory(c). \
        WhereElementIsNotElementType().ToElements()
    for e in elems:
        e_type = e.GetType().Name
        elem_type = doc.GetElement(e.GetTypeId())
        if e_type == "Wall":
            param = e.get_Parameter(BuiltInParameter.WALL_STRUCTURAL_SIGNIFICANT)
            param_func = elem_type.get_Parameter(BuiltInParameter.FUNCTION_PARAM)
            if param and param.AsInteger() == 1:
                result.append(SetWorkSet_byElement(e, '02_Стены'))
            elif param.AsInteger() == 0 and param_func.AsValueString() == 'Наружные слои':
                result.append(SetWorkSet_byElement(e, '01_Фасад'))
            elif param.AsInteger() == 0 and param_func.AsValueString() == 'Внутренние слои':
                result.append(SetWorkSet_byElement(e, '01_Перегородки'))
        elif e_type == 'Floor':
            param = e.get_Parameter(BuiltInParameter.FLOOR_PARAM_IS_STRUCTURAL)
            param_func = elem_type.get_Parameter(BuiltInParameter.FUNCTION_PARAM)
            if param and param.AsInteger() == 1:
                result.append(SetWorkSet_byElement(e, '02_Перекрытия'))
            elif param.AsInteger() == 0 and param_func.AsValueString() == 'Внутренние слои':
                result.append(SetWorkSet_byElement(e, '01_АрхПол'))

TransactionManager.Instance.TransactionTaskDone()

result.append(SetWorkSet_byCategory(BuiltInCategory.OST_Doors, '01_Двери'))
result.append(SetWorkSet_byCategory(BuiltInCategory.OST_Windows, '01_Окна'))
result.append(SetWorkSet_byCategory(BuiltInCategory.OST_StairsRailing, '02_Лестницы'))
result.append(SetWorkSet_byCategory(BuiltInCategory.OST_Stairs, '02_Лестницы'))
result.append(SetWorkSet_byCategory(BuiltInCategory.OST_Grids, '00_ОсиУровни'))
result.append(SetWorkSet_byCategory(BuiltInCategory.OST_Levels, '00_ОсиУровни'))
result.append(SetWorkSet_byCategory(BuiltInCategory.OST_CLines, '00_ОпорныеПлоскости'))
result.append(SetWorkSet_byCategory(BuiltInCategory.OST_Roofs, '01_Кровля'))
result.append(SetWorkSet_byCategory(BuiltInCategory.OST_StructuralColumns, '02_Колонны'))
result.append(SetWorkSet_byCategory(BuiltInCategory.OST_StructuralFraming, '02_Балки'))

OUT = result
