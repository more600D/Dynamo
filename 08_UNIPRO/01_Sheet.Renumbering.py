# -*- coding: utf-8 -*-
import clr
clr.AddReference("RevitAPI")
import Autodesk.Revit.DB as DB

clr.AddReference("RevitServices")
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager


doc = DocumentManager.Instance.CurrentDBDocument


def renumbering_sheets(sheets_col, separator, param_name):
	TransactionManager.Instance.EnsureInTransaction(doc)
	count = 0
	for sheet in sheets_col:
	    s_num =  sheet.SheetNumber
	    if separator in s_num:
	        res = s_num.split(separator)
	        param = sheet.LookupParameter(param_name)
	        if param:
	            param.Set(res[1])
	            count += 1
	TransactionManager.Instance.TransactionTaskDone()
	return 'Sheets are changed - {}'.format(count)


sep = IN[0]
param_name = IN[1]
sheets_col = DB.FilteredElementCollector(doc).OfClass(DB.ViewSheet).ToElements()

OUT = renumbering_sheets(sheets_col, sep, param_name)