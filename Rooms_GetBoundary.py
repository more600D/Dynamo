# -*- coding: utf-8 -*-
# Подключение библиотек
import clr
clr.AddReference("RevitAPI")
from Autodesk.Revit.DB import FilteredElementCollector, BuiltInCategory, SpatialElementBoundaryOptions
clr.AddReference("RevitServices")
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager

doc = DocumentManager.Instance.CurrentDBDocument

# Получение всех помещений в проекте
room_col = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Rooms).ToElements()

TransactionManager.Instance.EnsureInTransaction(doc)

# Работа со списком помещений
for room in room_col:
    value = 0
    opt = SpatialElementBoundaryOptions()
    boundaries_list = room.GetBoundarySegments(opt)  # Получение сегментов границ помещений
    for boundaries in boundaries_list:
        for b in boundaries:
            elem = doc.GetElement(b.ElementId)  # Получение элементов, которые являются границей помещения
            try:
                if elem.GetType().Name == "ModelLine":  # Проверка, является ли элемент "Разделителем помещения"
                    value += b.GetCurve().Length  # Если да, то получаем длину сегмента границы помещения
            except Exception:
                pass
    # Тут необходимо указать имя параметра для записи в него значения длины разделителей помещения
    param = room.LookupParameter('_Длина.РазделительПомещений')  # Получаем параметр помещения
    if param:  # Проверяем наличие параметра
        param.Set(value)  # Если есть, то записываем значение длины разделителя в параметр

TransactionManager.Instance.TransactionTaskDone()

OUT = room_col
