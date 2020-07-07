import clr
clr.AddReference("RevitAPI")
from Autodesk.Revit.DB import FilteredElementCollector, FilteredWorksetCollector, BuiltInCategory, WorksetKind, \
    BuiltInParameter, RevitLinkInstance
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
                    msg = 'Нет такого рабочего набора: {}'.format(name)
    else:
        msg = "Нет элементов категории {}".format(cat)
    return msg


def SetWorkSet_byElement(elem, name):
    param = elem.get_Parameter(BuiltInParameter.ELEM_PARTITION_PARAM)
    if param:
        worksetId = GetWorkSet(name)
        if worksetId:
            param.Set(worksetId)
            msg = 'ОК'
        else:
            msg = 'Нет такого рабочего набора: {}'.format(name)
    return msg


def SetWorkSet_byMaterial(cat, name_material, name_workset):
    elems = FilteredElementCollector(doc).OfCategory(cat).WhereElementIsNotElementType().ToElements()
    msges = []
    msges.append(str(cat).split('OST_')[1].upper())
    if elems:
        for e in elems:
            if e.GetType().Name != "FaceWall":
                e_type = doc.GetElement(e.GetTypeId())
                try:
                    layers = e_type.GetCompoundStructure().GetLayers()
                    for l in layers:
                        layer = doc.GetElement(l.MaterialId)
                        if layer:
                            if name_material.lower() in layer.Name.lower():
                                msg = SetWorkSet_byElement(e, name_workset) + ": {}".format(e.Name)
                                break
                            else:
                                msg = "Нет материала \"{}\": {}".format(name_material, e.Name)
                    msges.append(msg)
                except Exception:
                    pass
    else:
        msges.append('Нет элементов категории {}'.format(cat))
    return msges


def SetWorkSet_byGroupModel(cat):
    elems = FilteredElementCollector(doc).OfCategory(cat).WhereElementIsNotElementType().ToElements()
    msges = []
    for elem in elems:
        e_type = doc.GetElement(elem.GetTypeId())
        param = e_type.get_Parameter(BuiltInParameter.ALL_MODEL_MODEL)
        if param:
            param_value = param.AsString()
            if param_value:
                worksetId = GetWorkSet(param_value)
                if worksetId:
                    msg = SetWorkSet_byElement(elem, param_value)
            else:
                msg = 'Параметр пустой: {} id {}'.format(elem.Name, elem.Id)
        else:
            msg = 'Нет такого параметра'
        msges.append(msg)
    return msges


cats = []
cats.append(BuiltInCategory.OST_Walls)
cats.append(BuiltInCategory.OST_Floors)

result = []

# Стены и перекрытия
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


# Связи RVT
rvtLinks = FilteredElementCollector(doc).OfClass(RevitLinkInstance).ToElements()
for r in rvtLinks:
    if 'CO' in r.Name:
        result.append(SetWorkSet_byElement(r, '04_LevelsGrids'))
    elif 'KR' in r.Name:
        result.append(SetWorkSet_byElement(r, '04_KR'))

# Все остальное
result.append(SetWorkSet_byCategory(BuiltInCategory.OST_Lines, '99_Temp'))
result.append(SetWorkSet_byCategory(BuiltInCategory.OST_Doors, '01_Двери'))
result.append(SetWorkSet_byCategory(BuiltInCategory.OST_Windows, '01_Окна'))
result.append(SetWorkSet_byCategory(BuiltInCategory.OST_StairsRailing, '02_Лестницы'))
result.append(SetWorkSet_byCategory(BuiltInCategory.OST_Stairs, '01_Лестницы'))
result.append(SetWorkSet_byCategory(BuiltInCategory.OST_Grids, '00_ОсиУровни'))
result.append(SetWorkSet_byCategory(BuiltInCategory.OST_Levels, '00_ОсиУровни'))
result.append(SetWorkSet_byCategory(BuiltInCategory.OST_CLines, '00_ОпорныеПлоскости'))
result.append(SetWorkSet_byCategory(BuiltInCategory.OST_Roofs, '01_Кровля'))
result.append(SetWorkSet_byCategory(BuiltInCategory.OST_Fascia, '01_Кровля'))
result.append(SetWorkSet_byCategory(BuiltInCategory.OST_StructuralColumns, '02_Колонны'))
result.append(SetWorkSet_byCategory(BuiltInCategory.OST_StructuralFraming, '02_Балки'))
result.append(SetWorkSet_byCategory(BuiltInCategory.OST_Gutter, '01_ВодосточнаяСистема'))
result.append(SetWorkSet_byCategory(BuiltInCategory.OST_PipeCurves, '01_ВодосточнаяСистема'))
result.append(SetWorkSet_byCategory(BuiltInCategory.OST_PipeFitting, '01_ВодосточнаяСистема'))
result.append(SetWorkSet_byMaterial(BuiltInCategory.OST_Walls, 'Утеплитель', '01_Утепление'))
result.append(SetWorkSet_byMaterial(BuiltInCategory.OST_Walls, 'Штукатурка', '01_ВнутреняяОтделка'))
result.append(SetWorkSet_byMaterial(BuiltInCategory.OST_Floors, 'Утеплитель', '01_Утепление'))
result.append(SetWorkSet_byGroupModel(BuiltInCategory.OST_GenericModel))

TransactionManager.Instance.TransactionTaskDone()

OUT = result
