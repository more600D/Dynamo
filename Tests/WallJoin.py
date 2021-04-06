# -*- coding: utf-8 -*-
import clr
clr.AddReference("RevitAPI")
from Autodesk.Revit.DB import FilteredElementCollector, Wall, Outline, BoundingBoxIntersectsFilter, JoinGeometryUtils, \
    FamilyInstance, BuiltInCategory

clr.AddReference("RevitServices")
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager

doc = DocumentManager.Instance.CurrentDBDocument


def join_walls(collector):
    if collector:
        f_list = []
        for element in collector:
            group = []
            element_box = element.get_BoundingBox(None)
            if element_box:
                outline = Outline(element_box.Min, element_box.Max)
                bbfilter = BoundingBoxIntersectsFilter(outline)
                wall_col = FilteredElementCollector(doc).OfClass(Wall).WherePasses(bbfilter).ToElements()
                group.append(element)
                wall_host = element.Host
                for wall in wall_col:
                    group.append(wall)
                    try:
                        JoinGeometryUtils.JoinGeometry(doc, wall, wall_host)
                    except Exception:
                        pass
                f_list.append(group)
        return f_list


door_col = FilteredElementCollector(doc).OfClass(FamilyInstance).OfCategory(BuiltInCategory.OST_Doors)
window_col = FilteredElementCollector(doc).OfClass(FamilyInstance).OfCategory(BuiltInCategory.OST_Windows)

TransactionManager.Instance.EnsureInTransaction(doc)
f_list_door = join_walls(door_col)
f_list_windor = join_walls(window_col)
TransactionManager.Instance.TransactionTaskDone()

OUT = f_list_door, f_list_windor
