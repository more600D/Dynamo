# -*- coding: utf-8 -*-
# s.s.sh@mail.ru
import clr
clr.AddReference("RevitAPI")
from Autodesk.Revit.DB import Options, XYZ, UnitUtils, DisplayUnitType, StorageType, \
    FilteredElementCollector, BuiltInParameter
from Autodesk.Revit.DB.Architecture import Stairs
clr.AddReference("RevitServices")
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager


doc = DocumentManager.Instance.CurrentDBDocument
uiapp = DocumentManager.Instance.CurrentUIApplication
app = uiapp.Application


def get_type_name(elem):
    elem_type = doc.GetElement(elem.GetTypeId())
    elem_type_name = elem_type.get_Parameter(BuiltInParameter.SYMBOL_NAME_PARAM).AsString()
    return elem_type_name


def get_square_from_face(face):
    face_normal = face.FaceNormal
    if face_normal.IsAlmostEqualTo(XYZ.BasisZ):
        return face.Area
    else:
        return 0


def get_square_from_part(part_list, document):
    if part_list:
        square = 0
        for item_id in part_list:
            stair_run = document.GetElement(item_id)
            geometry = stair_run.get_Geometry(Options())
            if geometry:
                for geo in geometry:
                    if geo.GetType().Name == 'Solid':
                        for face in geo.Faces:
                            square += get_square_from_face(face)
                    if geo.GetType().Name == 'GeometryInstance' and square == 0:
                        instance_geo = geo.GetInstanceGeometry()
                        for solid in instance_geo:
                            for face in solid.Faces:
                                square += get_square_from_face(face)
            return square


def set_value(elem, parameter_name, value):
    param = elem.LookupParameter(parameter_name)
    if param:
        if param.StorageType == StorageType.String:
            param.Set(str(UnitUtils.ConvertFromInternalUnits(value,
                                                             DisplayUnitType.DUT_SQUARE_METERS)))
        else:
            param.Set(value)


def get_square_from_runs_and_landings(stair):
    if stair.Category.Id.IntegerValue == -2000120:
        document = stair.Document
        runs_square = get_square_from_part(stair.GetStairsRuns(), document)
        landings_square = get_square_from_part(stair.GetStairsLandings(), document)
        if runs_square:
            set_value(stair, IN[1], runs_square)  # noqa
            value_runs = UnitUtils.ConvertFromInternalUnits(runs_square,
                                                            DisplayUnitType.DUT_SQUARE_METERS)
        else:
            set_value(stair, IN[1], 0)  # noqa
            value_runs = 'нет маршей'
        if landings_square:
            set_value(stair, IN[2], landings_square)  # noqa
            value_landings = UnitUtils.ConvertFromInternalUnits(landings_square,
                                                                DisplayUnitType.DUT_SQUARE_METERS)
        else:
            set_value(stair, IN[2], 0)  # noqa
            value_landings = 'нет площадок'
        return 'Площадь ступенек: {}'.format(value_runs), 'Площадь площадок: {}'.format(value_landings)
    else:
        return 'Select stair'


stairs_col = FilteredElementCollector(doc).OfClass(Stairs)
result = []
TransactionManager.Instance.EnsureInTransaction(doc)
for stair in stairs_col:
    item = []
    item.append('Id лестницы: {}'.format(stair.Id))
    item.append('Имя: {}'.format(get_type_name(stair)))
    for square in get_square_from_runs_and_landings(stair):
        item.append(square)
    result.append(item)
TransactionManager.Instance.TransactionTaskDone()

OUT = result
