# -*- coding: utf-8 -*-
import clr
clr.AddReference("RevitAPI")
from Autodesk.Revit.DB import ViewType

clr.AddReference("RevitServices")
from RevitServices.Persistence import DocumentManager

doc = DocumentManager.Instance.CurrentDBDocument


elems = IN[1]

report = []
for elem in elems:
    uelem = UnwrapElement(elem)
    if uelem.Category.Name == 'Lines':
        view = doc.GetElement(uelem.OwnerViewId)
        view_type = view.ViewType
        if view_type != ViewType.Legend and view_type != ViewType.DraftingView:
            data = {
                'id': uelem.Id,
                'line_style': uelem.LineStyle.Name,
                'view_name': view.Name
            }
            report.append(data)
OUT = report