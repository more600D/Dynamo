import clr
clr.AddReference("RevitAPI")
from Autodesk.Revit.DB import FilteredElementCollector, BuiltInCategory, UnitUtils, ElementId
clr.AddReference('RevitAPIUI')
from Autodesk.Revit.UI.Selection import Selection
clr.AddReference("RevitServices")
from RevitServices.Persistence import DocumentManager
from System.Collections.Generic import List
doc = DocumentManager.Instance.CurrentDBDocument
uidoc = DocumentManager.Instance.CurrentUIApplication.ActiveUIDocument


def filterByParam(col, paramName):
    fList = []
    for i in col:
        param_group_model = i.Symbol.LookupParameter('Группа модели')
        if param_group_model:
            if param_group_model.AsString() == paramName:
                fList.append(i)
    return fList


def cutElements(col, paramName, value):
    result = []
    for i in col:
        if i.LookupParameter(paramName):
            para = i.LookupParameter(paramName)
            param_value = round(UnitUtils.ConvertFromInternalUnits(para.AsDouble(), para.DisplayUnitType))
            if param_value < value:
                result.append(i)
    return result


def selElements(col):
    elementIdList = List[ElementId]()
    for i in col:
        elementIdList.Add(i.Id)
    uidoc.Selection.SetElementIds(elementIdList)


col = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_GenericModel) \
    .WhereElementIsNotElementType().ToElements()

el = filterByParam(col, 'Чугунная плитка')

selElements(cutElements(el, 'Р_Длина', 1100))

OUT = cutElements(el, 'Р_Длина', 1100)
