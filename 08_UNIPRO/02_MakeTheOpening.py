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
        if family_name in fam_name:
            result.append(fam)
    return result


def set_time(fam_instance, mode=True, param_name='_Дата'):
    res = ''
    from datetime import datetime
    dt_string = datetime.now().strftime('%d.%m.%Y %H:%M:%S')
    param = fam_instance.LookupParameter(param_name)
    if param:
        if param.StorageType == DB.StorageType.String:
            if mode:
                if param.AsString() == '':
                    param.Set(dt_string)
            else:
                param.Set(dt_string)
    return dt_string


def cut_filtered_elements(class_type, bb_filter, family):
    count = 0
    elems_col = DB.FilteredElementCollector(doc)\
                  .OfClass(class_type)\
                  .WherePasses(bb_filter)\
                  .ToElements()
    if elems_col:
        for f in elems_col:
            try:
                DB.InstanceVoidCutUtils.AddInstanceVoidCut(doc, f, family)
                count += 1
                set_time(family, False)
            except: pass
    return count


def cut_elements(fams):
    TransactionManager.Instance.EnsureInTransaction(doc)
    floors = 0
    walls = 0
    roofs = 0
    if fams:
        for fam in fams:
            current_time = set_time(fam)
            bbox = fam.get_BoundingBox(None)
            bb_filter = DB.BoundingBoxIntersectsFilter(
                        DB.Outline(bbox.Min, bbox.Max)
                        )
            floors += cut_filtered_elements(DB.Floor, bb_filter, fam)
            walls += cut_filtered_elements(DB.Wall, bb_filter, fam)
            roofs += cut_filtered_elements(DB.FootPrintRoof, bb_filter, fam)
        TransactionManager.Instance.TransactionTaskDone()
        result = 'Cutted elements - {}'.format(floors + walls + roofs)
        data = result+'\n'+current_time
        return data
    else: return 'Family list is empty'


name = IN[1]
OUT = cut_elements(get_family_opening(name))