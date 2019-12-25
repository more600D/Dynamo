# -*- coding: utf-8 -*-
import clr
clr.AddReference("RevitAPI")
from Autodesk.Revit.DB import FilteredElementCollector, BuiltInParameter
from Autodesk.Revit.DB.Architecture import Railing, PatternJustification
clr.AddReference("RevitServices")
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager


doc = DocumentManager.Instance.CurrentDBDocument
uiapp = DocumentManager.Instance.CurrentUIApplication
app = uiapp.Application


def GetTypeRailing(items, document):
    types = []
    info = []
    for item in items:
        param_length = item.get_Parameter(BuiltInParameter.CURVE_ELEM_LENGTH)
        railingType = document.GetElement(item.GetTypeId())
        bp = railingType.BalusterPlacement.BalusterPattern
        info.append(bp.DistributionJustification)
        if bp.DistributionJustification == PatternJustification.Beginning or \
                bp.DistributionJustification == PatternJustification.End:
            types.append(int(param_length.AsDouble() / bp.Length))
        elif bp.DistributionJustification == PatternJustification.Center:
            types.append(int(param_length.AsDouble() / bp.Length) + 2)
        elif bp.DistributionJustification == PatternJustification.SpreadPatternToFit:
            types.append(int(param_length.AsDouble() / bp.Length) - 2)
    return types, info


el = FilteredElementCollector(doc).OfClass(Railing).ToElements()

OUT = GetTypeRailing(el, doc)
