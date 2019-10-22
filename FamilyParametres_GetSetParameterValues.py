import clr
clr.AddReference('RevitAPI')
from Autodesk.Revit.DB import *

clr.AddReference('RevitServices')
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager

docs = IN[0]
param_list = []
param_values = []
cats = []
familytypecount = []

for doc in docs:
	#setup familydoc files
	uiapp = DocumentManager.Instance.CurrentUIApplication
	familydoc = uiapp.Application.OpenDocumentFile(doc)
	params = familydoc.FamilyManager.GetParameters()
	ps = familydoc.FamilyManager.get_Parameter(IN[1])
	types = familydoc.FamilyManager.Types
	famMan = familydoc.FamilyManager
	
	#parameters, categories from family files
	names = [p.Definition.Name for p in params]
	param_list.append(names)
	cats.append(familydoc.OwnerFamily.FamilyCategory.Name)
	
	#FAMILY TYPES
	#add "Default" type in families with no types
	familytypecount.append(types.Size)
	if familytypecount < 1:
		TransactionManager.Instance.EnsureInTransaction(familydoc)
		new_fam=famMan.NewType('Default')
		TransactionManager.Instance.ForceCloseTransaction()
	#get Assembly Code from types
	TransactionManager.Instance.EnsureInTransaction(familydoc)
	familyTypesItor = famMan.Types.ForwardIterator()
	familyTypesItor.Reset()
	while (familyTypesItor.MoveNext()):
		#get current value
		familyParam = famMan.get_Parameter(IN[1])
		familyType = familyTypesItor.Current
		param_values.append(familyType.AsString(familyParam))
	TransactionManager.Instance.ForceCloseTransaction()

#output
OUT = cats,param_list,familytypecount,param_values
