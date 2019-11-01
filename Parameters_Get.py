import clr
clr.AddReference('RevitAPI')
from Autodesk.Revit.DB import *
from Autodesk.Revit.DB.Electrical import *

clr.AddReference('RevitServices')
from RevitServices.Persistence import DocumentManager

doc = DocumentManager.Instance.CurrentDBDocument
lightItems = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_LightingFixtures).WhereElementIsNotElementType().ToElements()

lightFixture = [i for i in lightItems]
elivation = [int(i.LookupParameter('О_Отметка').AsValueString()) for i in lightItems]

OUT = lightItems, elivation
