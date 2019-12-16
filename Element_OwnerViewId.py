import clr
clr.AddReference("RevitAPI")
from Autodesk.Revit.DB import FilteredElementCollector, FamilyInstance
clr.AddReference("RevitServices")
from RevitServices.Persistence import DocumentManager

doc = DocumentManager.Instance.CurrentDBDocument

el = FilteredElementCollector(doc).OfClass(FamilyInstance).ToElements()

ch = []
vw = []
uniqView = []
for i in el:
    if i.Symbol.FamilyName == '16_ТХ_Стул':
        ch.append(i)
        vwId = i.OwnerViewId
        vw.append((doc.GetElement(vwId)))

OUT = vw, vwId
