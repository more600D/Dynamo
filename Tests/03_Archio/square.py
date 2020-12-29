# -*- coding: utf-8 -*-
import clr
clr.AddReference("RevitAPI")
from Autodesk.Revit.DB import Options, UnitUtils, DisplayUnitType
clr.AddReference("RevitServices")
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager


doc = DocumentManager.Instance.CurrentDBDocument
uiapp = DocumentManager.Instance.CurrentUIApplication
app = uiapp.Application


def GetVolumeFromBBox(el):
    bbox = sel.get_BoundingBox(None)
    bbox_lenght = bbox.Max.X - bbox.Min.X
    bbox_width = bbox.Max.Y - bbox.Min.Y
    bbox_height = bbox.Max.Z - bbox.Min.Z
    return bbox_height * bbox_width * bbox_lenght


sel = UnwrapElement(IN[1])  # noqa
faces = []
square = 0

solids = sel.get_Geometry(Options())
bbox = GetVolumeFromBBox(sel)
if solids:
    for solid in solids:
        sol = solid.Volume
        if hasattr(solid, 'Faces'):
            for face in solid.Faces:
                mat_id = face.MaterialElementId
                if mat_id.IntegerValue == -1:
                    square += face.Area

# sq = UnitUtils.ConvertFromInternalUnits(square, DisplayUnitType.DUT_SQUARE_METERS)
# vol = UnitUtils.ConvertFromInternalUnits(sol, DisplayUnitType.DUT_CUBIC_METERS)

OUT = UnitUtils.ConvertFromInternalUnits(bbox, DisplayUnitType.DUT_CUBIC_METERS)
