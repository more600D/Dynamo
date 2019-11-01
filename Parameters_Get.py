import clr
clr.AddReference('RevitAPI')
from Autodesk.Revit.DB import FilteredElementCollector, BuiltInCategory
clr.AddReference('RevitServices')
from RevitServices.Persistence import DocumentManager


def create_elevation(param_name):
    return [int(i.LookupParameter(param_name).AsValueString()) for i in lightItems]


doc = DocumentManager.Instance.CurrentDBDocument
lightItems = FilteredElementCollector(doc) \
    .OfCategory(BuiltInCategory.OST_LightingFixtures) \
    .WhereElementIsNotElementType() \
    .ToElements()


OUT = lightItems, create_elevation('О_Отметка')