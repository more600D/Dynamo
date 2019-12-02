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


col = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_GenericModel) \
    .WhereElementIsNotElementType().ToElements()

p1 = 'Р_Длина'

el_filtered = filterByParam(col, 'Чугунная плитка')
el_cutted = cutElements(el_filtered, p1, 1100)

p_list = []
part = []
# for i in el_cutted:
#     partValue = 1100
#     para = i.LookupParameter(p1)
#     if para:
#         while partValue >= 0:
#             value = round(UnitUtils.ConvertFromInternalUnits(para.AsDouble(), para.DisplayUnitType))
#             if partValue >= 0:
#                 part.append(i)
#                 partValue -= value
#         else:
#             part = []
#     p_list.append(part)

# for i in range(len(el_cutted)):
#     for j[i] in el_cutted:
partValue = 1100
more_haft = []
less_haft = []
for i in el_cutted:
    para = i.LookupParameter(p1)
    value = round(UnitUtils.ConvertFromInternalUnits(para.AsDouble(), para.DisplayUnitType))
    if para:
        if value > partValue / 2:
            more_haft.append(i)
        else:
            less_haft.append(i)

for i in more_haft:
    i_para = i.LookupParameter(p1)
    i_value = round(UnitUtils.ConvertFromInternalUnits(i_para.AsDouble(), i_para.DisplayUnitType))
    result = 0
    if i_para:
        for j in less_haft:
            j_para = j.LookupParameter(p1)
            j_value = round(UnitUtils.ConvertFromInternalUnits(j_para.AsDouble(), j_para.DisplayUnitType))
            if j_para:
                if result + j_value < partValue - i_value:
                    

OUT = more_haft, less_haft
