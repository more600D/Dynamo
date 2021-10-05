from collections import Counter
import clr
clr.AddReference("RevitAPI")
from Autodesk.Revit.DB import FilteredElementCollector, Options, BuiltInParameter, BuiltInCategory
from Autodesk.Revit.DB.Architecture import Railing
clr.AddReference("RevitServices")
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager


doc = DocumentManager.Instance.CurrentDBDocument


def to_meters(data):
    return '{:.2f}'.format(round(float(data) / 1000, 2))


def get_data_handrail_type(handrail_type, railing_length):
    pr_mark = handrail_type.get_Parameter(BuiltInParameter.WINDOW_TYPE_ID).AsString()
    p_length1 = handrail_type.get_Parameter(
        BuiltInParameter.CONTINUOUSRAIL_END_EXTENSION_LENGTH_PARAM).AsValueString()
    p_length2 = handrail_type.get_Parameter(
        BuiltInParameter.CONTINUOUSRAIL_EXTENSION_LENGTH_PARAM).AsValueString()
    full_length = float(p_length1) + float(p_length2) + float(railing_length)
    height_param = handrail_type.get_Parameter(BuiltInParameter.HANDRAIL_HEIGHT_PARAM)
    if height_param:
        height = height_param.AsValueString()
        return '\r\n{} (L={}, h={})'.format(pr_mark, to_meters(full_length), to_meters(height))
    else:
        return '\r\n{} (L={}'.format(pr_mark, to_meters(full_length))


def get_all_hand_rail_type(railing):
    data = ''
    check = 'несчитать'
    doc = railing.Document
    railing_length = railing.get_Parameter(BuiltInParameter.CURVE_ELEM_LENGTH).AsValueString()
    railing_type = doc.GetElement(railing.GetTypeId())
    primary_handrail_type = doc.GetElement(railing_type.PrimaryHandrailType)
    primary_handrail_type_name = primary_handrail_type.get_Parameter(BuiltInParameter.SYMBOL_NAME_PARAM).AsString()
    primary_handrail_pos = railing_type.PrimaryHandRailPosition
    secondary_handrail_type = doc.GetElement(railing_type.SecondaryHandrailType)
    secondary_handrail_type_name = secondary_handrail_type.get_Parameter(BuiltInParameter.SYMBOL_NAME_PARAM).AsString()
    secondary_handrail_pos = railing_type.SecondaryHandRailPosition
    top_rail_type = doc.GetElement(railing_type.TopRailType)
    top_rail_type_name = top_rail_type.get_Parameter(BuiltInParameter.SYMBOL_NAME_PARAM).AsString()
    if not primary_handrail_pos and not secondary_handrail_pos and not top_rail_type:
        data = '-'
    else:
        if top_rail_type and check not in top_rail_type_name.lower():
            tr_height = railing_type.get_Parameter(
                BuiltInParameter.RAILING_SYSTEM_TOP_RAIL_HEIGHT_PARAM).AsValueString()
            value = get_data_handrail_type(top_rail_type, railing_length) + ', h={})'.format(to_meters(tr_height))
            data += value
        if primary_handrail_pos and check not in primary_handrail_type_name.lower():
            data += get_data_handrail_type(primary_handrail_type, railing_length)
        if secondary_handrail_pos and check not in secondary_handrail_type_name.lower():
            data += get_data_handrail_type(secondary_handrail_type, railing_length)
    if check in top_rail_type_name.lower() and check in primary_handrail_type_name.lower() and \
        check in secondary_handrail_type_name.lower():
        data = '-'
    return data.strip()
 

def get_all_balusters(railing):
    geos = railing.get_Geometry(Options())
    geo_instance = []
    for g in geos:
        if g.GetType().Name == "GeometryInstance":
            for symbol_geo in g.GetSymbolGeometry():
                if symbol_geo.GetType().Name == "GeometryInstance":
                    geo_instance.append(symbol_geo.Symbol) 
    return geo_instance


def get_data_balusters(doc, balusters_list, type_name):
    list_type = []
    data = ''
    all_type_balusters = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_StairsRailingBaluster)
    for b in balusters_list:
        b_name = b.get_Parameter(BuiltInParameter.SYMBOL_NAME_PARAM).AsString()
        for b_type in all_type_balusters:
            b_type_name = b_type.get_Parameter(BuiltInParameter.SYMBOL_NAME_PARAM).AsString()
            b_type_group_model = b_type.get_Parameter(BuiltInParameter.ALL_MODEL_MODEL)
            if b_type_group_model:
                value = b_type_group_model.AsString()
                if b_name == b_type_name and value == type_name:
                    list_type.append(b_type.get_Parameter(BuiltInParameter.WINDOW_TYPE_ID).AsString())
    counts_dict = Counter(sorted(list_type))
    if list_type:
        for c in list(counts_dict):
            data += '\r\n{} ({}шт)'.format(c, counts_dict[c])
    else:
        data = '-'
    return data.strip()


def set_to_parameter(param_name, data):
    param = railing.LookupParameter(param_name)
    if param:
        param.Set(data)


TransactionManager.Instance.EnsureInTransaction(doc)
railing_col = FilteredElementCollector(doc).OfClass(Railing)
for railing in railing_col:
    set_to_parameter('_Поручень', get_all_hand_rail_type(railing))
    set_to_parameter('_Стойка', get_data_balusters(doc, get_all_balusters(railing), 'Стойка'))
    set_to_parameter('_Панель', get_data_balusters(doc, get_all_balusters(railing), 'Панель'))
TransactionManager.Instance.TransactionTaskDone()

OUT = list(railing_col)
