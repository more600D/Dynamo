# -*- coding: utf-8 -*-
from itertools import groupby
import clr
clr.AddReference("RevitAPI")
from Autodesk.Revit.DB import ElementClassFilter, ElementType, BuiltInParameter, Options

clr.AddReference("RevitServices")
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager


doc = DocumentManager.Instance.CurrentDBDocument
uiapp = DocumentManager.Instance.CurrentUIApplication
app = uiapp.Application

elem = UnwrapElement(IN[1])  # noqa


def group_by_key(elems, keyfunc):
    items = []
    keys = []
    for key, group in groupby(sorted(elems, key=keyfunc), key=keyfunc):
        items.append(list(group))
        keys.append(key)
    return items


def get_element_type(type_ids, name):
    for t in type_ids:
        elem = doc.GetElement(t)
        param = elem.get_Parameter(BuiltInParameter.ALL_MODEL_TYPE_NAME)
        if param.AsString() == name:
            return elem


def get_geometry_instances(elem):
    geo_instance = []
    geo = elem.get_Geometry(Options())
    for g in geo:
        if g.GetType().Name == 'GeometryInstance':
            geo_instance.append(g)
    return geo_instance


def get_balusters_structure(elem):
    geometry_instances = get_geometry_instances(elem)
    result = group_by_key(geometry_instances,
                          lambda x: x.Symbol.Family.Id.IntegerValue)
    f_list = []
    for i in range(0, len(result)):
        info = group_by_key(result[i],
                            lambda x: x.Symbol.get_Parameter(BuiltInParameter.ALL_MODEL_TYPE_NAME).AsString())
        f_list.append(info)
    balusters = ''
    num = 1
    for family_list in f_list:
        for elem_types in family_list:
            count = len(elem_types)
            family_name = elem_types[0].Symbol.Family.Name
            symbol_name = elem_types[0].Symbol.get_Parameter(BuiltInParameter.ALL_MODEL_TYPE_NAME).AsString()
            balusters += '\r\n{} - {}:{} - {}шт.'.format(num, family_name, symbol_name, count)
            num += 1
    return balusters.strip()


def set_to_parameter(elem, value, built_in_parameter_name=BuiltInParameter.ALL_MODEL_INSTANCE_COMMENTS):
    param = elem.get_Parameter(built_in_parameter_name)
    if param:
        param.Set(value)
        return 'Everething is awesome'


def set_to_type_parameter(elem, value, built_in_parameter_name=BuiltInParameter.ALL_MODEL_TYPE_COMMENTS):
    elem_type = doc.GetElement(elem.GetTypeId())
    return set_to_parameter(elem_type, value, built_in_parameter_name)


class_filter = ElementClassFilter(ElementType)
elements_type_id = elem.GetDependentElements(class_filter)
element_type = get_element_type(elements_type_id, 'Railing')

structure = get_balusters_structure(element_type)
baluster_count = len(get_geometry_instances(element_type))

TransactionManager.Instance.EnsureInTransaction(doc)
a = set_to_parameter(elem, str(baluster_count))
b = set_to_type_parameter(elem, structure)
TransactionManager.Instance.TransactionTaskDone()

# OUT = structure, 'Общее количество - {}шт.'.format(baluster_count)
OUT = a, b
