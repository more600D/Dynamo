import clr
clr.AddReference("RevitAPI")
from Autodesk.Revit.DB import FilteredElementCollector, FamilyInstance, BuiltInCategory, BuiltInParameter, Outline, \
    BoundingBoxIntersectsFilter, Wall, InstanceVoidCutUtils
clr.AddReference("RevitServices")
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager


doc = DocumentManager.Instance.CurrentDBDocument

all_panels = FilteredElementCollector(doc).OfClass(FamilyInstance). \
    OfCategory(BuiltInCategory.OST_CurtainWallPanels).ToElements()

TransactionManager.Instance.EnsureInTransaction(doc)
win_panels = []
for p in all_panels:
    fam_name = p.Symbol.get_Parameter(BuiltInParameter.SYMBOL_NAME_PARAM).AsString()
    if "05_ОкноСФрамугой_Витраж" in fam_name:
        pan_box = p.get_BoundingBox(None)
        if pan_box:
            outline = Outline(pan_box.Min, pan_box.Max)
            bbfilter = BoundingBoxIntersectsFilter(outline)
            intersects = FilteredElementCollector(doc).OfClass(Wall).WherePasses(bbfilter).ToElements()
            for i in intersects:
                if i.Name != IN[1]:
                    try:
                        InstanceVoidCutUtils.AddInstanceVoidCut(doc, i, p)
                    except: pass
            win_panels.append(p)
TransactionManager.Instance.TransactionTaskDone()

OUT = win_panels
