import clr

# Import Element wrapper extension methods
clr.AddReference("RevitNodes")
import Revit
clr.ImportExtensions(Revit.Elements)

# Import DocumentManager and TransactionManager
clr.AddReference("RevitServices")
import RevitServices
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager

doc = DocumentManager.Instance.CurrentDBDocument

# Import RevitAPI
clr.AddReference("RevitAPI")
import Autodesk
from Autodesk.Revit.DB import *

import sys
pyt_path = r'C:\Program Files (x86)\IronPython 2.7\Lib'
sys.path.append(pyt_path)

def ProcessList(_func, _list):
    return map( lambda x: ProcessList(_func, x) if type(x)==list else _func(x), _list )

names = [i for j in IN[0] for i in j]

def CreateWorkset(name):
	doc = DocumentManager.Instance.CurrentDBDocument
	try:
		w = Workset.Create(doc, name)
	except:
		# if error accurs anywhere in the process catch it
		import traceback
		w = traceback.format_exc()
	return w
	
try:
	errorReport = None
	if not doc.IsWorkshared:
		errorReport = "Функция Совместной работы не активна"
	else:
		TransactionManager.Instance.EnsureInTransaction(doc)
		newWorksets = ProcessList(CreateWorkset, names)
		TransactionManager.Instance.TransactionTaskDone()

except:
	# if error accurs anywhere in the process catch it
	import traceback
	errorReport = traceback.format_exc()

#Assign your output to the OUT variable
if errorReport == None:
	OUT = newWorksets
else:
	OUT = '\n'.join('{:^35}'.format(s) for s in errorReport.split('\n'))
