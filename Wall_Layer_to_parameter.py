# -*- coding: utf-8 -*-
import clr
clr.AddReference("RevitAPI")
from Autodesk.Revit.DB import UnitUtils, DisplayUnitType, StorageType, ElementClassFilter, \
    IndependentTag, BuiltInParameter

clr.AddReference("RevitServices")
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager


doc = DocumentManager.Instance.CurrentDBDocument


def to_int(float_num):
    num_parts = str(float_num).split('.')
    if int(num_parts[1]) == 0:
        return int(float_num)
    else:
        return float_num


def get_material_name(material_id, param_name):
    mat = doc.GetElement(material_id)
    if mat:
        param = mat.LookupParameter(param_name)
        if param:
            if param.StorageType == StorageType.String:
                return param.AsString()
    else:
        return 'The material is not assigned'


def get_max_slab_shape_vertex(structure_element):
    if structure_element.Category.Id.IntegerValue == -2000032:
        slab_shape_editor = structure_element.SlabShapeEditor
        if slab_shape_editor:
            slab_shape_vertices = slab_shape_editor.SlabShapeVertices
            point_z = [vertice.Position.Z for vertice in slab_shape_vertices]
            return UnitUtils.ConvertFromInternalUnits(max(point_z), DisplayUnitType.DUT_MILLIMETERS)
    else:
        return 'no shape editor'


def get_layers_to_string(structure_element, element_param_name, material_param_name, base=''):
    element_type = doc.GetElement(structure_element.GetTypeId())
    element_param = element_type.LookupParameter(element_param_name)
    if element_param:
        structure = element_type.GetCompoundStructure()
        variable_layer_index = structure.VariableLayerIndex
        max_point = get_max_slab_shape_vertex(structure_element)
        layers = structure.GetLayers()
        data = ''
        for i in range(0, len(layers)):
            width = to_int(UnitUtils.ConvertFromInternalUnits(layers[i].Width, DisplayUnitType.DUT_MILLIMETERS))
            name = get_material_name(layers[i].MaterialId, material_param_name).capitalize()
            if not name:
                name = 'Value_is_missing'
            is_variable_layer = layers[i].LayerId == variable_layer_index
            if width != 0 and not is_variable_layer or isinstance(max_point, str):
                data += '\r\n{}. {} - {} мм'.format(i + 1, name, width)
            elif is_variable_layer and not isinstance(max_point, str):
                total_width = to_int(width + max_point)
                data += '\r\n{}. {} - от {}-{} мм'.format(i + 1, name, width, total_width)
            else:
                data += '\r\n{}. {}'.format(i + 1, name)
        if base:
            data += '\r\n{}. {}'.format(len(layers) + 1, base)
        if element_param.StorageType == StorageType.String:
            element_param.Set(data.strip())
        return data.strip()


def get_independent_tag_by_name(tag_ids, name):
    for tag_id in tag_ids:
        elem = doc.GetElement(tag_id)
        fam_name = elem.get_Parameter(BuiltInParameter.ELEM_FAMILY_PARAM).AsValueString()
        if name in fam_name:
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


def change_type_tag(data, tag):
    if tag and data:
        layers = data.split('\r\n')
        types = tag.GetValidTypes()
        count = len(layers)
        t = get_type_tag(types, count)
        tag.ChangeTypeId(t)
        return 'Everything is awesome'


element = UnwrapElement(IN[1])  # noqa
element_parameter_to_set = IN[2]  # noqa
material_info = IN[3]  # noqa
last_layer = ''
TransactionManager.Instance.EnsureInTransaction(doc)
data = get_layers_to_string(element, element_parameter_to_set, material_info, last_layer)  # noqa
change_type_tag(data, get_tag(element))
TransactionManager.Instance.TransactionTaskDone()

OUT = data
