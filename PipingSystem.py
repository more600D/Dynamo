import clr
clr.AddReference("RevitAPI")
from Autodesk.Revit.DB import FilteredElementCollector, UnitUtils
from Autodesk.Revit.DB.Plumbing import PipingSystem
clr.AddReference("RevitServices")
from RevitServices.Persistence import DocumentManager

doc = DocumentManager.Instance.CurrentDBDocument

sys = FilteredElementCollector(doc).OfClass(PipingSystem)

paramValue = []
for s in sys:
    sysType = doc.GetElement(s.GetTypeId())
    param = sysType.LookupParameter('Температура вещества')
    if param:
        value = param.AsDouble()
        paramValue.append(round(UnitUtils.ConvertFromInternalUnits(value, param.DisplayUnitType)))

OUT = paramValue
