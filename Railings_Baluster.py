# -*- coding: utf-8 -*-
import clr
clr.AddReference("RevitAPI")
from Autodesk.Revit.DB import FilteredElementCollector, BuiltInParameter, UnitUtils, DisplayUnitType
from Autodesk.Revit.DB.Architecture import Railing, PatternJustification
clr.AddReference("RevitServices")
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager


doc = DocumentManager.Instance.CurrentDBDocument
uiapp = DocumentManager.Instance.CurrentUIApplication
app = uiapp.Application


def AnglePath(items):
    result = []
    angles = []
    for item in items:
        path = item.GetPath()
        result.append(path)
        og = []
        for p in path:
            points = []
            pt0 = p.GetEndPoint(0)
            pt1 = p.GetEndPoint(1)
            points.append(pt1)
            points.append(pt0)
            og.append(points)
        angles.append(og)
    return result, angles


def GetBalisterCount(items, document):
    types = []
    info = []
    for item in items:
        param_length = item.get_Parameter(BuiltInParameter.CURVE_ELEM_LENGTH)
        railingType = document.GetElement(item.GetTypeId())
        bp = railingType.BalusterPlacement.BalusterPattern
        cornerPost = railingType.BalusterPlacement.PostPattern
        cornerPost_el = doc.GetElement(cornerPost.CornerPost.BalusterFamilyId)
        info.append(UnitUtils.ConvertFromInternalUnits(bp.PatternAngle, DisplayUnitType.DUT_DEGREES_AND_MINUTES))
        if bp.DistributionJustification == PatternJustification.Beginning or \
                bp.DistributionJustification == PatternJustification.End:
            count = int(param_length.AsDouble() / bp.Length)
        elif bp.DistributionJustification == PatternJustification.Center:
            count = int(param_length.AsDouble() / bp.Length) + 2
        elif bp.DistributionJustification == PatternJustification.SpreadPatternToFit:
            count = int(param_length.AsDouble() / bp.Length) - 2
        if cornerPost_el:
            count += 1
        types.append(count)

    return types, info


el = FilteredElementCollector(doc).OfClass(Railing).ToElements()

OUT = AnglePath(el)
