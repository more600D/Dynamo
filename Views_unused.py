import clr
clr.AddReference("RevitAPI")
from Autodesk.Revit.DB import FilteredElementCollector, View, Viewport, ViewType, BuiltInCategory
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


def not_on_sheet(firstlist, secondlist):
    return [doc.GetElement(r) for r in list(set(firstlist) - set(secondlist))]


views_col = FilteredElementCollector(doc).OfClass(View).ToElements()
view_port = FilteredElementCollector(doc).OfClass(Viewport).ToElements()
schedule_graf = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_ScheduleGraphics)

view_list = []
schedule_list = []
view_TreeD = []
view_DraftingView = []
view_Section = []
view_FloorPlan = []
view_Legend = []
view_Schedule = []
copyName = []

for v in views_col:
    if v.ViewType == ViewType.ThreeD and not v.IsTemplate:
        if '{' and '}' not in v.Name:
            view_TreeD.append(v.Id)
    if v.ViewType == ViewType.DraftingView and not v.IsTemplate:
        if v.Name != "Стартовый лист":
            view_DraftingView.append(v.Id)
    if v.ViewType == ViewType.Section and not v.IsTemplate:
        view_Section.append(v.Id)
    if v.ViewType == ViewType.FloorPlan and not v.IsTemplate:
        view_FloorPlan.append(v.Id)
    if v.ViewType == ViewType.Legend and not v.IsTemplate:
        view_Legend.append(v.Id)
    if v.ViewType == ViewType.Schedule and not v.IsTemplate:
        if '000_' not in v.Name:
            view_Schedule.append(v.Id)
    if 'копия' in v.Name:
        copyName.append(v)
for p in view_port:
    view_list.append(p.ViewId)
for p in schedule_graf:
    schedule_list.append(p.ScheduleId)

u_TreeD = not_on_sheet(view_TreeD, view_list)
u_DraftingView = not_on_sheet(view_DraftingView, view_list)
u_Section = not_on_sheet(view_Section, view_list)
u_FloorPlan = not_on_sheet(view_FloorPlan, view_list)
u_Legend = not_on_sheet(view_Legend, view_list)
u_Schedule = not_on_sheet(view_Schedule, schedule_list)

OUT = u_TreeD, u_DraftingView, u_Section, u_FloorPlan, u_Legend, u_Schedule, copyName, not_null(views_col)
