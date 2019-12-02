import clr
clr.AddReference("RevitAPI")
from Autodesk.Revit.DB import FilteredElementCollector, BuiltInCategory, UnitUtils, DisplayUnitType
clr.AddReference("RevitServices")
from RevitServices.Persistence import DocumentManager
doc = DocumentManager.Instance.CurrentDBDocument


def filterByParam(col, paramName):
    fList = []
    for i in col:
        param_group_model = i.Symbol.LookupParameter('Группа модели')
        if param_group_model:
            if param_group_model.AsString() == paramName:
                fList.append(i)
    return fList


def cutElements(col, paramName):
    result = []
    for i in col:
        if i.LookupParameter(paramName):
            para = i.LookupParameter(paramName)
            param_value = round(UnitUtils.ConvertFromInternalUnits(para.AsDouble(), para.DisplayUnitType))
            if param_value < 1100:
                result.append(i)
    return result


col = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_GenericModel) \
    .WhereElementIsNotElementType().ToElements()

el = filterByParam(col, 'Чугунная плитка')


OUT = cutElements(el, 'Р_Длина'), el
