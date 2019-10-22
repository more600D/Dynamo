import clr
import System

clr.AddReference('RevitAPI')
import Autodesk
from Autodesk.Revit.DB import *

clr.AddReference('RevitServices')
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager

uiapp = DocumentManager.Instance.CurrentUIApplication
doc = DocumentManager.Instance.CurrentDBDocument

mypath = IN[0]
docs = []
fams = System.IO.Directory.GetFiles(mypath)
fams2 = []

# Flatten list
params = [j for sub in IN[3] for j in sub] 

for i in fams:
	if IN[1] == True: #Если True, то выбираются все файлы файлы в папке
		fams2.append(i)
	elif IN[2] in i: #Если содержит значение в IN[2], то выбираются семейства удовлетворяющие значению
		fams2.append(i)
for doc in fams2:
	familydoc = uiapp.Application.OpenDocumentFile(doc)#Открытие семейств
	docs.append(familydoc)

for f in docs:
	t = Transaction(f, 'Добавление параметров') #Открытие транзакции
	family_manager = f.FamilyManager #Получение FamilyManager
	t.Start()
	for p in params:
		family_manager.AddParameter(p, BuiltInParameterGroup.PG_TEXT, ParameterType.Text, True) #Добавление параметров
	t.Commit()

OUT = docs, params
