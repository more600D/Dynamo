import clr
clr.AddReference("RevitAPI")
from Autodesk.Revit.DB import FilteredElementCollector, View, Viewport, ViewType
clr.AddReference("RevitServices")
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager


doc = DocumentManager.Instance.CurrentDBDocument
uiapp = DocumentManager.Instance.CurrentUIApplication
app = uiapp.Application


def not_null(el):
    result = []
    for i in el:
        if i and not i.IsTemplate:
            result.append(i)
    return result


views_col = FilteredElementCollector(doc).OfClass(View).ToElements()
view_port = FilteredElementCollector(doc).OfClass(Viewport).ToElements()

view_list = []
view_3d_on = []

for v in views_col:
    if v.ViewType == ViewType.ThreeD and not v.IsTemplate:
        view_3d_on.append(v.Id)
for p in view_port:
    view_list.append(p.ViewId)

result = [doc.GetElement(r) for r in list(set(view_3d_on) - set(view_list))]

OUT = result, not_null(views_col)
