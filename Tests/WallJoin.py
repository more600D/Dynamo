# -*- coding: utf-8 -*-
import clr
clr.AddReference("RevitAPI")
from Autodesk.Revit.DB import FilteredElementCollector, Wall, Outline, BoundingBoxIntersectsFilter, JoinGeometryUtils, \
    FamilyInstance, BuiltInCategory

clr.AddReference("RevitServices")
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager

doc = DocumentManager.Instance.CurrentDBDocument

door_col = FilteredElementCollector(doc).OfClass(FamilyInstance).OfCategory(BuiltInCategory.OST_Doors)

f_list = []

TransactionManager.Instance.EnsureInTransaction(doc)

if door_col:
    for door in door_col:
        group = []
        door_box = door.get_BoundingBox(None)
        if door_box:
            outline = Outline(door_box.Min, door_box.Max)
            bbfilter = BoundingBoxIntersectsFilter(outline)
            wall_col = FilteredElementCollector(doc).OfClass(Wall).WherePasses(bbfilter).ToElements()
            group.append(door)
            wall_host = door.Host
            for wall in wall_col:
                group.append(wall)
                try:
                    JoinGeometryUtils.JoinGeometry(doc, wall, wall_host)
                except Exception:
                    pass
            f_list.append(group)

TransactionManager.Instance.TransactionTaskDone()

OUT = f_list
