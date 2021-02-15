# -*- coding: utf-8 -*-
import clr
clr.AddReference("RevitAPI")
from Autodesk.Revit.DB import UnitUtils, DisplayUnitType, StorageType, ElementClassFilter, \
    IndependentTag, BuiltInParameter

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
        return 'The material is not assigned'


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
            if not name:
                name = 'Value_is_missing'
            if width != 0:
                data += '\r\n{}. {} - {} мм'.format(i + 1, name.capitalize(), width)
            else:
                data += '\r\n{}. {}'.format(i + 1, name.capitalize())
        if element_param.StorageType == StorageType.String:
            element_param.Set(data.strip())
        return data.strip()


def get_independent_tag_by_name(tag_ids, name):
    for tag_id in tag_ids:
        elem = doc.GetElement(tag_id)
        fam_name = elem.get_Parameter(BuiltInParameter.ELEM_FAMILY_PARAM).AsValueString()
        if fam_name == name:
            return elem


def get_tag(elem):
    independ_tags_class = ElementClassFilter(IndependentTag)
    tags = elem.GetDependentElements(independ_tags_class)
    tag = get_independent_tag_by_name(tags, 'Марка_флажок')
    return tag


def get_type_tag(types, number):
    for t in types:
        elem = doc.GetElement(t)
        name = elem.get_Parameter(BuiltInParameter.SYMBOL_NAME_PARAM).AsString()
        if str(number) in name:
            return t


def change_type_tag(elem, tag):
    element_type = doc.GetElement(elem.GetTypeId())
    structure = element_type.GetCompoundStructure()
    types = tag.GetValidTypes()
    if structure:
        count = structure.LayerCount
        t = get_type_tag(types, count)
        tag.ChangeTypeId(t)
        return 'Everything is awesome'


sel = UnwrapElement(IN[1])  # noqa

TransactionManager.Instance.EnsureInTransaction(doc)
data = get_layers_to_string(sel, IN[2], IN[3])  # noqa
change_type_tag(sel, get_tag(sel))
TransactionManager.Instance.TransactionTaskDone()

OUT = data
