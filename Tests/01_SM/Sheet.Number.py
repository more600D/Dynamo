# -*- coding: utf-8 -*-
import clr
clr.AddReference("RevitAPI")
from Autodesk.Revit.DB import FilteredElementCollector, ViewSheet
clr.AddReference("RevitServices")
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager

doc = DocumentManager.Instance.CurrentDBDocument

sheet_col = FilteredElementCollector(doc).OfClass(ViewSheet).ToElements()

info = []
filter_name = IN[1]  # noqa
separator = IN[2]  # noqa
param_name = IN[3]  # noqa

TransactionManager.Instance.EnsureInTransaction(doc)

if sheet_col:
    for s in sheet_col:
        if filter_name in s.Title:
            sheet_num = s.SheetNumber.split(separator)
            param = s.LookupParameter(param_name)
            if param:
                param.Set(sheet_num[1])
                info.append('{} заменент на {}'.format(s.SheetNumber, sheet_num[1]))
            else:
                info.append('Нет такого параметра')

TransactionManager.Instance.TransactionTaskDone()

OUT = info
