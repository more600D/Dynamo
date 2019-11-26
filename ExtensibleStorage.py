import clr
clr.AddReference("RevitAPI")
from Autodesk.Revit.DB import FilteredElementCollector, ProjectInfo
from Autodesk.Revit.DB.ExtensibleStorage import Schema
clr.AddReference("RevitServices")
from RevitServices.Persistence import DocumentManager


def flat_list(lists):
    flat = []
    for sublist in lists:
        for item in sublist:
            flat.append(item)
    return flat


doc = DocumentManager.Instance.CurrentDBDocument

info = FilteredElementCollector(doc).OfClass(ProjectInfo).ToElements()
item_guid = [i.GetEntitySchemaGuids() for i in info]

sc = Schema.ListSchemas()

for s in sc:
    if s.GUID == flat_list(item_guid)[0]:
        project_schema = s

en = [i.GetEntity(project_schema) for i in info]

OUT = en
