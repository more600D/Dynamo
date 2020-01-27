import clr
clr.AddReference("RevitAPI")
from Autodesk.Revit.DB import FilteredElementCollector, View3D, Viewport
clr.AddReference("RevitServices")
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager


doc = DocumentManager.Instance.CurrentDBDocument
uiapp = DocumentManager.Instance.CurrentUIApplication
app = uiapp.Application

views_col = FilteredElementCollector(doc).OfClass(View3D).ToElements()
view_port = FilteredElementCollector(doc).OfClass(Viewport).ToElements()

view_list = []
view_3d_on = []

for v in views_col:
    if v and not v.IsTemplate:
        view_3d_on.append(v.Id)
for p in view_port:
    view_list.append(p.ViewId)

result = [doc.GetElement(r) for r in list(set(view_3d_on) - set(view_list))]

OUT = result
