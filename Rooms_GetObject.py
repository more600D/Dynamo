# -*- coding: utf-8 -*-
import clr
clr.AddReference("RevitAPI")
from Autodesk.Revit.DB import FilteredElementCollector, Options, BuiltInCategory, XYZ, UnitUtils, DisplayUnitType
clr.AddReference("RevitNodes")
from Revit.GeometryConversion import RevitToProtoCurve
clr.AddReference("RevitServices")
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager


doc = DocumentManager.Instance.CurrentDBDocument


room_col = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Rooms).ToElements()
opt = Options()
opt.View = doc.ActiveView
opt.IncludeNonVisibleObjects = True
lines = []
for r in room_col:
    for g in r.get_Geometry(opt):
        if 'Line' in g.ToString():
            vector = (g.GetEndPoint(1) - g.GetEndPoint(0)).Normalize()
            degrees = UnitUtils.ConvertFromInternalUnits(vector.AngleTo(XYZ.BasisX), \
                DisplayUnitType.DUT_DECIMAL_DEGREES)
            if round(degrees) == 135:
                lines.append(RevitToProtoCurve.ToProtoType(g))

OUT = room_col, lines
