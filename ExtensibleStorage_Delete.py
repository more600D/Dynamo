import clr
clr.AddReference("RevitAPI")
from Autodesk.Revit.DB import FilteredElementCollector, ProjectInfo
from Autodesk.Revit.DB.ExtensibleStorage import Schema
clr.AddReference("RevitServices")
from RevitServices.Persistence import DocumentManager

doc = DocumentManager.Instance.CurrentDBDocument


def __flatten__(lists):
    flat_list = []
    for sublist in lists:
        for item in sublist:
            flat_list.append(item)
    return flat_list


info = FilteredElementCollector(doc).OfClass(ProjectInfo).ToElements()
item_guid = [i.GetEntitySchemaGuids() for i in info]

sch = [Schema.Lookup(i) for i in __flatten__(item_guid)]

OUT = sch
