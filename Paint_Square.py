# -*- coding: utf-8 -*-
import clr
clr.AddReference("RevitAPI")
from Autodesk.Revit.DB import Options, ElementId, UnitUtils, DisplayUnitType
clr.AddReference("RevitServices")
from RevitServices.Persistence import DocumentManager

from itertools import groupby

doc = DocumentManager.Instance.CurrentDBDocument


def RemovePaintFromElement(el):
    solids = UnwrapElement(el).get_Geometry(Options())  # noqa
    if solids:
        painted_face = []
        for solid in solids:
            if hasattr(solid, "Faces"):
                for face in solid.Faces:
                    elID = ElementId(el.Id)
                    if doc.IsPainted(elID, face):
                        painted_face.append(face)
                    if face.HasRegions:
                        for regFace in face.GetRegions():
                            if doc.IsPainted(elID, regFace):
                                painted_face.append(regFace)
        return painted_face


def group_by_key(elems, keyfunc):
    sorted_group = []
    keys = []
    for key, group in groupby(sorted(elems, key=keyfunc), key=keyfunc):
        sorted_group.append(list(group))
        keys.append(key)
    return sorted_group, keys


sel = IN[1]  # noqa

if isinstance(sel, list):
    painted_face = []
    for s in sel:
        pf = RemovePaintFromElement(s)
        if pf:
            painted_face.append(pf)
    all_faces = []
    for items in painted_face:
        for item in items:
            all_faces.append(item)

    list_elems = group_by_key(all_faces, lambda e: e.MaterialElementId)[0]

    faces_area = []
    for items in list_elems:
        fa = []
        for item in items:
            fa.append(UnitUtils.ConvertFromInternalUnits(item.Area, DisplayUnitType.DUT_SQUARE_METERS))
        faces_area.append(fa)

    list_name = group_by_key(all_faces, lambda e: doc.GetElement(e.MaterialElementId).Name)[1]

    OUT = faces_area, list_name
else:
    OUT = RemovePaintFromElement(sel)
