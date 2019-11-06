import clr
clr.AddReference("RevitServices")
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager


doc = DocumentManager.Instance.CurrentDBDocument
uiapp = DocumentManager.Instance.CurrentUIApplication
app = uiapp.Application

file = app.OpenSharedParameterFile()

fp = doc.FamilyManager.get_Parameter(IN[0])

myExtDef = file.Groups.get_Item(IN[2]).Definitions.get_Item(IN[1]) 

TransactionManager.Instance.EnsureInTransaction(doc)
doc.FamilyManager.ReplaceParameter(fp, myExtDef, fp.Definition.ParameterGroup, fp.IsInstance)
TransactionManager.Instance.TransactionTaskDone()

OUT = 'Готово'
