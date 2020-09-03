# -*- coding: utf-8 -*-
import clr
clr.AddReference("RevitAPI")
from Autodesk.Revit.DB import FilteredElementCollector, Options, Material, ElementId
clr.AddReference("RevitServices")
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager

doc = DocumentManager.Instance.CurrentDBDocument
uiapp = DocumentManager.Instance.CurrentUIApplication
app = uiapp.Application


def GetMaterail(name):
    mat_col = FilteredElementCollector(doc).OfClass(Material)
    for m in mat_col:
        if name == m.Name:
            return m


def AddPaint(old_Mat, new_Mat, face, elem):
    if old_Mat == doc.GetElement(face.MaterialElementId).Name:
        doc.Paint(ElementId(elem.Id), face, GetMaterail(new_Mat).Id)
        return "Готово!"
    else:
        return "Нет - {}".format(old_Mat)


sel = IN[1]  # noqa
old_Mat = IN[2]  # noqa
new_Mat = IN[3]  # noqa
all_mat = list()

TransactionManager.Instance.EnsureInTransaction(doc)
if isinstance(sel, list):
    for s in sel:
        solid_list = UnwrapElement(s).get_Geometry(Options())  # noqa
        for solid in solid_list:
            if hasattr(solid, "Faces"):
                for face in solid.Faces:
                    all_mat.append(doc.GetElement(face.MaterialElementId).Name)
                    AddPaint(old_Mat, new_Mat, face, s)
                    if face.HasRegions:
                        regions = face.GetRegions()
                        for regFace in regions:
                            all_mat.append(doc.GetElement(regFace.MaterialElementId).Name)
                            AddPaint(old_Mat, new_Mat, regFace, s)
TransactionManager.Instance.TransactionTaskDone()

OUT = all_mat
