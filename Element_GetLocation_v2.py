import clr
clr.AddReference("RevitAPI")
from Autodesk.Revit.DB import FilteredElementCollector, RevitLinkInstance, BuiltInCategory
clr.AddReference("RevitServices")
from RevitServices.Persistence import DocumentManager


doc = DocumentManager.Instance.CurrentDBDocument


def __flatten__(lists):
    flat_list = []
    for sublist in lists:
        for item in sublist:
            flat_list.append(item)
    return flat_list


rvt_links = FilteredElementCollector(doc).OfClass(RevitLinkInstance).ToElements()

rvt_lights = []
for r in rvt_links:
    if "03-01_" in r.Name:
        rvt_lights.append(r)

ldoc = [r.GetLinkDocument() for r in rvt_lights]

lights = []
for l in ldoc:
    item = []
    el = FilteredElementCollector(l).OfCategory(BuiltInCategory.OST_LightingFixtures) \
        .WhereElementIsNotElementType().ToElements()
    item.append(el)
    lights.append(item)


OUT = lights[0]


uniq = [1,2,3,4,5]
fifa = ['a','b','c','d','e']
uniq_and_fifa = dict(zip(uniq, fifa))
print(uniq_and_fifa)
