import clr
clr.AddReference('RevitAPI')
from Autodesk.Revit.DB import FilteredElementCollector, BuiltInCategory
clr.AddReference('RevitServices')
from RevitServices.Persistence import DocumentManager


def all_of_category():
    return FilteredElementCollector(doc) \
        .OfCategory(BuiltInCategory.OST_LightingFixtures) \
        .WhereElementIsNotElementType()


def value_elevation(param_name, items):
    return [int(i.LookupParameter(param_name).AsValueString()) for i in items]


doc = DocumentManager.Instance.CurrentDBDocument

items_lights = [i for i in all_of_category()]

OUT = items_lights, value_elevation('О_Отметка', items_lights)
