# -*- coding: utf-8 -*-
import clr
clr.AddReference("RevitAPI")
from Autodesk.Revit.DB import Options, ElementId

clr.AddReference("RevitServices")
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager

doc = DocumentManager.Instance.CurrentDBDocument


def RemovePaintFromElement(el):
    solids = UnwrapElement(el).get_Geometry(Options())  # noqa
    if solids:
        for solid in solids:
            if hasattr(solid, "Faces"):
                for face in solid.Faces:
                    selID = ElementId(el.Id)
                    doc.RemovePaint(selID, face)
                    if face.HasRegions:
                        regions = face.GetRegions()
                        for regFace in regions:
                            doc.RemovePaint(selID, regFace)
sel = IN[1]  # noqa

TransactionManager.Instance.EnsureInTransaction(doc)

if isinstance(sel, list):
    for s in sel:
        RemovePaintFromElement(s)
else:
    RemovePaintFromElement(sel)

TransactionManager.Instance.TransactionTaskDone()

OUT = sel
