# -*- coding: utf-8 -*-
import clr
clr.AddReference("RevitAPI")
from Autodesk.Revit.DB import IFamilyLoadOptions, Sweep, FilteredElementCollector, UnitUtils, Options, \
    Transaction, FamilySource
clr.AddReference("RevitServices")
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager


doc = DocumentManager.Instance.CurrentDBDocument
uiapp = DocumentManager.Instance.CurrentUIApplication
app = uiapp.Application


class FamilyOption(IFamilyLoadOptions):
    def OnFamilyFound(self, familyInUse, overwriteParameterValues):
        self.overwriteParameterValues = True
        return True

    def OnSharedFamilyFound(self, sharedFamily, familyInUse, source, overwriteParameterValues):
        self.source = FamilySource.Family
        self.overwriteParameterValues = True
        return True


def get_volume_from_bBox(element):
    bbox = element.get_BoundingBox(None)
    bbox_lenght = bbox.Max.X - bbox.Min.X
    bbox_width = bbox.Max.Y - bbox.Min.Y
    bbox_height = bbox.Max.Z - bbox.Min.Z
    return bbox_height * bbox_width * bbox_lenght


def get_square_from_solid(element):
    square = 0
    volume = 0
    solids = element.get_Geometry(Options())
    if solids:
        for solid in solids:
            volume += solid.Volume
            if hasattr(solid, 'Faces'):
                for face in solid.Faces:
                    mat_id = face.MaterialElementId
                    if mat_id.IntegerValue == -1:
                        square += face.Area
        return square, volume


def set_parameter_by_name(value, param_name, document):
    f_manager = document.FamilyManager
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


element = UnwrapElement(IN[1])  # noqa

family = element.Symbol.Family
TransactionManager.Instance.ForceCloseTransaction()
fam_doc = doc.EditFamily(family)
if fam_doc:

    family_manager = fam_doc.FamilyManager
    sweep_col = FilteredElementCollector(fam_doc).OfClass(Sweep).ToElements()
    sweep = [s for s in list(sweep_col) if s.IsSolid][0]

    param_ARH_l = family_manager.get_Parameter('ARH_l')

    trans = Transaction(fam_doc, 'запись')
    trans.Start()
    if param_ARH_l:
        family_manager.Set(param_ARH_l, UnitUtils.ConvertToInternalUnits(1000, param_ARH_l.DisplayUnitType))
    square = get_square_from_solid(sweep)[0]
    vol1 = get_square_from_solid(sweep)[1]
    vol2 = get_volume_from_bBox(sweep)
    sq = set_parameter_by_name(square, 'ARH_sr', fam_doc)
    volume1 = set_parameter_by_name(vol1, 'ARH_v1', fam_doc)
    volume2 = set_parameter_by_name(vol2, 'ARH_v2', fam_doc)
    trans.Commit()
    fam_doc.LoadFamily(doc, FamilyOption())
    fam_doc.Close(False)

OUT = param_ARH_l
