import clr
clr.AddReference("RevitAPI")
from Autodesk.Revit.DB import FilteredElementCollector, View, ViewType
clr.AddReference("RevitServices")
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager


doc = DocumentManager.Instance.CurrentDBDocument
uiapp = DocumentManager.Instance.CurrentUIApplication
app = uiapp.Application

view_col = FilteredElementCollector(doc).OfClass(View).ToElements()

TransactionManager.Instance.EnsureInTransaction(doc)

views = []
view_withoutTemlate = []
for v in view_col:
    if not v.IsTemplate:
        if 'копия' in v.Name:
            name = v.Name.split('копия')
            add = 'Переименовать!!!'
            new_name = '{} {}'.format(name[0], add.upper())
            views.append(v)
            v.Name = new_name
        if v.ViewType == ViewType.FloorPlan:
            view_withoutTemlate.append(v)
        elif v.ViewType == ViewType.ThreeD:
            view_withoutTemlate.append(v)
        elif v.ViewType == ViewType.AreaPlan:
            view_withoutTemlate.append(v)
        elif v.ViewType == ViewType.Section:
            view_withoutTemlate.append(v)
        elif v.ViewType == ViewType.CeilingPlan:
            view_withoutTemlate.append(v)
        elif v.ViewType == ViewType.EngineeringPlan:
            view_withoutTemlate.append(v)
        for vw in view_withoutTemlate:
            param = vw.LookupParameter('VW_НазначениеВида')
            if param:
                if doc.GetElement(vw.ViewTemplateId) is None:
                    param.Set('Без_Шаблона'.upper())
                else:
                    try:
                        param.Set('')
                    except: pass

TransactionManager.Instance.TransactionTaskDone()

OUT = view_withoutTemlate
