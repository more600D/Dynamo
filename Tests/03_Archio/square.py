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


def SetParameterByName(value, param_name):
    f_manager = doc.FamilyManager
    param = f_manager.get_Parameter(param_name)
    if param:
        f_manager.Set(param, value)
        return 'OK'
    else:
        return 'Not OK'


sel = UnwrapElement(IN[1])  # noqa
faces = []
square = 0
vol1 = 0

vol2 = GetVolumeFromBBox(sel)

solids = sel.get_Geometry(Options())
if solids:
    for solid in solids:
        vol1 += solid.Volume
        if hasattr(solid, 'Faces'):
            for face in solid.Faces:
                mat_id = face.MaterialElementId
                if mat_id.IntegerValue == -1:
                    square += face.Area

sq = UnitUtils.ConvertFromInternalUnits(square, DisplayUnitType.DUT_SQUARE_METERS)
volume1 = UnitUtils.ConvertFromInternalUnits(vol1, DisplayUnitType.DUT_CUBIC_METERS)
volume2 = UnitUtils.ConvertFromInternalUnits(vol2, DisplayUnitType.DUT_CUBIC_METERS)

TransactionManager.Instance.EnsureInTransaction(doc)

SetParameterByName(square, 'ARH_sr')
SetParameterByName(vol1, 'ARH_v1')
SetParameterByName(vol2, 'ARH_v2')

TransactionManager.Instance.TransactionTaskDone()
OUT = sq, volume1, volume2
