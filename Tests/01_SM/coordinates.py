# -*- coding: utf-8 -*-
import sys
pyt_path = r'C:\Program Files (x86)\IronPython 2.7\Lib'
sys.path.append(pyt_path)
import os
import datetime
import clr
clr.AddReference("RevitAPI")
from Autodesk.Revit.DB import FilteredElementCollector, BuiltInCategory
clr.AddReference("RevitServices")
from RevitServices.Persistence import DocumentManager

doc = DocumentManager.Instance.CurrentDBDocument

# Получение координат точек элементов категории "Осветительные приборы"
elems = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_LightingFixtures). \
    WhereElementIsNotElementType().ToElements()
points = []
for el in elems:
    pt = str(el.Location.Point)[1:]
    pt = pt[:len(pt) - 1]
    points.append(pt)

# Создание имени и пути файла
date = datetime.datetime.today().strftime("%Y%m%d_%H%M%S")
filename = "Coordinates_{}.csv".format(date)
path = r'C:\Users\sssh\OneDrive\Desktop\test'
fullpath = os.path.join(path, filename)

# Запись координат
with open(fullpath, 'w') as file:
    for p in points:
        file.write(p + '\n')

OUT = points
