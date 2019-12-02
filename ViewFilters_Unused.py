import clr
clr.AddReference("RevitAPI")
from Autodesk.Revit.DB import FilteredElementCollector, View, ViewType, ParameterFilterElement
clr.AddReference("RevitServices")
from RevitServices.Persistence import DocumentManager
doc = DocumentManager.Instance.CurrentDBDocument


def floorPlans(col):
    ap = []
    for v in col:
        if v.ViewType == ViewType.FloorPlan and not v.IsTemplate:
            ap.append(v)
    return ap


def flattenList(self):
    f_list = []
    for s in self:
        for i in s:
            f_list.append(i)
    return f_list


colView = FilteredElementCollector(doc).OfClass(View).ToElements()
colFilters = FilteredElementCollector(doc).OfClass(ParameterFilterElement).ToElements()

useFilter_Ids = [i.GetFilters() for i in floorPlans(colView)]
useFilter = [doc.GetElement(f).Name for f in flattenList(useFilter_Ids)]

unUsed = []
for f in colFilters:
    if f.Id not in flattenList(useFilter_Ids):
        unUsed.append(doc.GetElement(f.Id).Name)

OUT = unUsed
