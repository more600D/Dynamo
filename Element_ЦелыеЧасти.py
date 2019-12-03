import clr
clr.AddReference("RevitAPI")
from Autodesk.Revit.DB import FilteredElementCollector, BuiltInCategory, UnitUtils, ElementId
clr.AddReference("RevitServices")
from RevitServices.Persistence import DocumentManager
from System.Collections.Generic import List
doc = DocumentManager.Instance.CurrentDBDocument
uidoc = DocumentManager.Instance.CurrentUIApplication.ActiveUIDocument


def filterByParam(col, paramValue):  # Фильтрация элементов по параметру Группа моделей
    fList = []
    for i in col:
        param_group_model = i.Symbol.LookupParameter('Группа модели')
        if param_group_model:
            if param_group_model.AsString() == paramValue:
                fList.append(i)
    return fList


def cutElements(col, paramName, value):  # Получение список плиток меньше значения value из paramName
    result = []
    for i in col:
        para = i.LookupParameter(paramName)
        if para:
            param_value = round(UnitUtils.ConvertFromInternalUnits(para.AsDouble(), para.DisplayUnitType))
            if param_value < value:
                result.append(i)
    return result


def selElements(col):  # Выделение элементов из списка ElementId
    elementIdList = List[ElementId]()
    for i in col:
        elementIdList.Add(i.Id)
    uidoc.Selection.SetElementIds(elementIdList)


def valueParameter(param, paramName):
    para = param.LookupParameter(paramName)
    return round(UnitUtils.ConvertFromInternalUnits(para.AsDouble(), para.DisplayUnitType))


col = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_GenericModel) \
    .WhereElementIsNotElementType().ToElements()

p1 = 'Р_Длина'

el_filtered = filterByParam(col, 'Чугунная плитка')
el_cutted = cutElements(el_filtered, p1, 1100)

more_haft = []
less_haft = []
partValue = 1100

for i in el_cutted:
    para = i.LookupParameter(p1)
    value = valueParameter(i, p1)
    if para:
        if value > partValue / 2:
            more_haft.append(i)
        else:
            less_haft.append(i)

p_list = []

for i in more_haft:
    i_value = valueParameter(i, p1)
    if i.LookupParameter(p1):
        part = []
        for j in less_haft:
            j_value = valueParameter(j, p1)
            if j.LookupParameter(p1):
                if i_value + j_value > partValue:
                    part.append(i)
    p_list.append(part)

OUT = p_list
