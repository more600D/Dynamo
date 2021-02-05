# -*- coding: utf-8 -*-
import clr
clr.AddReference("RevitAPI")
from Autodesk.Revit.DB import Options, UnitUtils
clr.AddReference("RevitServices")
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager
clr.AddReference("RevitNodes")
from Revit.GeometryConversion import RevitToProtoSolid, ProtoToRevitSolid
from Revit.Elements import Element

doc = DocumentManager.Instance.CurrentDBDocument


def GetVolumeFromBBox(el):
    bbox = sel.get_BoundingBox(None)
    bbox_lenght = bbox.Max.X - bbox.Min.X
    bbox_width = bbox.Max.Y - bbox.Min.Y
    bbox_height = bbox.Max.Z - bbox.Min.Z
    return bbox_height * bbox_width * bbox_lenght


def SetParameterByName(value, param_name):
    f_manager = doc.FamilyManager
    if len(list(f_manager.Types)) == 0:
        f_manager.NewType('Тип 1')
    param = f_manager.get_Parameter(param_name)
    if param:
        if param.CanAssignFormula:
            val = UnitUtils.ConvertFromInternalUnits(value, param.DisplayUnitType)
            f_manager.SetFormula(param, str(val))
            return '{} - {}'.format(param_name, val)
    else:
        return 'Not OK'


sel = UnwrapElement(IN[1])  # noqa
faces = []
square = 0
vol1 = 0

solids = sel.get_Geometry(Options())
if solids:
    for solid in solids:
        a = RevitToProtoSolid.ToProtoType(solid)
        vol1 += solid.Volume
        if hasattr(solid, 'Faces'):
            for face in solid.Faces:
                mat_id = face.MaterialElementId
                if mat_id.IntegerValue == -1:
                    square += face.Area

vol2 = GetVolumeFromBBox(sel)

TransactionManager.Instance.EnsureInTransaction(doc)

sq = SetParameterByName(square, 'ARH_sr')
volume1 = SetParameterByName(vol1, 'ARH_v1')
volume2 = SetParameterByName(vol2, 'ARH_v2')

TransactionManager.Instance.TransactionTaskDone()

OUT = sq, volume1, volume2
