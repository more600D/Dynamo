import clr
clr.AddReference('RevitAPI')
from Autodesk.Revit.DB import *
clr.AddReference("RevitServices")
from RevitServices.Persistence import DocumentManager

dataEnteringNode = IN
doc = DocumentManager.Instance.CurrentDBDocument

#Функции
def FinalList(list1, list2):
	result = []
	for item in list1:
		if not item in list2:
			result.append(item)
	return result
#------------------------------------
errors = []
workset_name = IN[1]

worksets = FilteredWorksetCollector(doc).OfKind(WorksetKind.UserWorkset).ToWorksets()
UserWorksets_names = []

for name in worksets:
	UserWorksets_names.append(name.Name)

result = FinalList(workset_name, UserWorksets_names)

try:
	report = "Выполнено!"
	if not doc.IsWorkshared:
		report = "Функция совместной работы не активна"
	elif len(result)==0:
		report = "Все рабочие наборы уже имеются"
	else:
		t = Transaction(doc)
		t.Start("Создание рабочих наборов")
		for name in result:
			Workset.Create(doc, name)
		t.Commit()
except Exception as err:
		errors.append(err)

OUT = report, errors, result
