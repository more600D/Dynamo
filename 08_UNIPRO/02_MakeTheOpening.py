# -*- coding: utf-8 -*-
import clr
clr.AddReference("RevitAPI")
import Autodesk.Revit.DB as DB

clr.AddReference("RevitServices")
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager


doc = DocumentManager.Instance.CurrentDBDocument


def get_family_opening(family_name):
    result = []
    collector = DB.FilteredElementCollector(doc)\
                  .OfClass(DB.FamilyInstance)\
                  .ToElements()
    for fam in collector:
        fam_name = fam.Symbol.Family.Name
        if fam_name == family_name:
            result.append(fam)
    return result


def cut_elements(fams):
    count = 0
    TransactionManager.Instance.EnsureInTransaction(doc)
    for fam in fams:
        bbox = fam.get_BoundingBox(None)
        bb_filter = DB.BoundingBoxIntersectsFilter(
                       DB.Outline(bbox.Min, bbox.Max)
                       )
        floor_col = DB.FilteredElementCollector(doc)\
                      .OfClass(DB.Floor)\
                      .WherePasses(bb_filter)\
                      .ToElements()
        if floor_col:
            for f in floor_col:
                try:
                    DB.InstanceVoidCutUtils.AddInstanceVoidCut(doc, f, fam)
                    count += 1
                except: pass
    TransactionManager.Instance.TransactionTaskDone()
    return 'Elements cutted - {}'.format(count)


name = 'UNI_Openning.Floor'
OUT = cut_elements(get_family_opening(name))