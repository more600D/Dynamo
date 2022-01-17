# -*- coding: utf-8 -*-
from itertools import groupby
import clr
clr.AddReference("RevitAPI")
from Autodesk.Revit.DB import FilteredElementCollector, BuiltInCategory, UnitUtils, BuiltInParameter
clr.AddReference("RevitServices")
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager


doc = DocumentManager.Instance.CurrentDBDocument


def filter_rooms(collector):
    """Фильтрация помещений. Получения всех размещенных и окруженных помещений"""
    rooms_in_project = []
    for c in collector:
        if c.Location and c.Area > 0:
            rooms_in_project.append(c)
    return rooms_in_project


def convert_room_square(room):
    """Конвертация из внутренних единиц в квадратные метры"""
    version = int(room.Document.Application.VersionNumber)
    param = room.get_Parameter(BuiltInParameter.ROOM_AREA)
    if version > 2021:
        return UnitUtils.ConvertFromInternalUnits(param.AsDouble(), param.GetUnitTypeId())
    else:
        return UnitUtils.ConvertFromInternalUnits(param.AsDouble(), param.DisplayUnitType)


def get_list_name_rooms(data):
    data_list = []
    for d in data.split(','):
        data_list.append(d.strip().lower())
    return data_list


def set_parameter_by_name(elem, name, value):
    param = elem.LookupParameter(name)
    if param:
        param.Set(value)


def set_room_squares(room, number, ratio):
    set_parameter_by_name(room, 'ADSK_Тип помещения', number)
    set_parameter_by_name(room, 'ADSK_Коэффициент площади', ratio)
    set_parameter_by_name(room, 'ADSK_Площадь с коэффициентом', room.Area * ratio)


def get_all_living_rooms(collector, living, notliving):
    data_living = get_list_name_rooms(living)
    data_notliving = get_list_name_rooms(notliving)
    for room in collector:
        room_param_name = room.get_Parameter(BuiltInParameter.ROOM_NAME)
        room_name = room_param_name.AsString()
        if room_name.lower() in data_living:
            set_room_squares(room, 1, 1)
        elif room_name.lower() in data_notliving:
            set_room_squares(room, 2, 1)
        elif room_name.lower() == 'лоджия':
            set_room_squares(room, 3, 0.5)
        elif room_name.lower() == 'балкон':
            set_room_squares(room, 4, 0.3)
        else:
            set_room_squares(room, 5, 1)


def group_by_key(elems, keyfunc):
    items = []
    keys = []
    for key, group in groupby(sorted(elems, key=keyfunc), key=keyfunc):
        items.append(list(group))
        keys.append(key)
    return items


def get_app_number(room, name='ADSK_Номер квартиры'):
    room_app_number = room.LookupParameter(name)
    if room_app_number:
        room_app_number_value = room_app_number.AsString()
        if room_app_number_value != '':
            return room_app_number_value


def set_room_data(app_list):
    count_living_rooms = 0
    square_ratio = 0
    square_living = 0
    area = 0
    for room in app_list:
        type_room_param = room.LookupParameter('ADSK_Тип помещения')
        if type_room_param: 
            if type_room_param.AsInteger() == 1:
                count_living_rooms += 1
                square_living += room.Area
        squqre_with_ratio_param = room.LookupParameter('ADSK_Площадь с коэффициентом')
        if squqre_with_ratio_param:
            square_ratio += squqre_with_ratio_param.AsDouble()
            if type_room_param:
                if type_room_param.AsInteger() < 3:
                    area += squqre_with_ratio_param.AsDouble()
    
    for room in app_list:
        set_parameter_by_name(room, 'ADSK_Количество комнат', count_living_rooms)
        set_parameter_by_name(room, 'ADSK_Площадь квартиры жилая', square_living)
        set_parameter_by_name(room, 'ADSK_Площадь квартиры общая', square_ratio)
        set_parameter_by_name(room, 'ADSK_Площадь квартиры', area)


room_col = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Rooms)
# OUT = [convert_room_square(r) for r in filter_rooms(room_col)]

TransactionManager.Instance.EnsureInTransaction(doc)

get_all_living_rooms(room_col, IN[1], IN[2])
apps = group_by_key(list(room_col), get_app_number)

for app in apps:
    set_room_data(app)

TransactionManager.Instance.TransactionTaskDone()

OUT = apps[1:]
