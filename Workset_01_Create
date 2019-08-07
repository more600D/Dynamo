import clr
clr.AddReference('RevitAPI')
from Autodesk.Revit.DB import *
clr.AddReference("RevitServices")
from RevitServices.Persistence import DocumentManager

dataEnteringNode = IN
doc = DocumentManager.Instance.CurrentDBDocument
errors = []
workset_name = IN[1]
try:
	report = "Выполнено!"
	if not doc.IsWorkshared:
		report = "Функция совместной работы не активна"
	else:
		t = Transaction(doc)
		t.Start("Создание рабочих наборов")
		for name in workset_name:
			Workset.Create(doc, name)
		t.Commit()
except Exception as err:
		errors.append(err)
OUT = report, errors
