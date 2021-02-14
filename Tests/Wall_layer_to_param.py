# -*- coding: utf-8 -*-
import clr
clr.AddReference("RevitAPI")
from Autodesk.Revit.DB import UnitUtils, DisplayUnitType, StorageType

clr.AddReference("RevitServices")
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager


doc = DocumentManager.Instance.CurrentDBDocument


def get_material_name(material_id, param_name):
    mat = doc.GetElement(material_id)
    if mat:
        param = mat.LookupParameter(param_name)
        if param:
            if param.StorageType == StorageType.String:
                return param.AsString()
    else:
        return 'Материал не назначен'


def get_layers_to_string(structure_element, element_param_name, material_param_name):
    element_type = doc.GetElement(structure_element.GetTypeId())
    element_param = element_type.LookupParameter(element_param_name)
    if element_param:
        structure = element_type.GetCompoundStructure()
        layers = structure.GetLayers()
        data = ''
        for i in range(0, len(layers)):
            width = UnitUtils.ConvertFromInternalUnits(layers[i].Width, DisplayUnitType.DUT_MILLIMETERS)
            name = get_material_name(layers[i].MaterialId, material_param_name)
            data += '\r\n{}. {} - {} мм'.format(i + 1, name, width)
        if element_param.StorageType == StorageType.String:
            element_param.Set(data.strip())
        return data.strip()


sel = UnwrapElement(IN[1])  # noqa

TransactionManager.Instance.EnsureInTransaction(doc)
data = get_layers_to_string(sel, IN[2], IN[3])  # noqa
TransactionManager.Instance.TransactionTaskDone()

OUT = data
