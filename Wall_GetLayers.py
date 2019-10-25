import clr
clr.AddReference('RevitAPI')
from Autodesk.Revit.DB import *

clr.AddReference("RevitServices")
import RevitServices
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager

doc = DocumentManager.Instance.CurrentDBDocument

def _Concat(name,count):
	listName = []
	for i in range(1, count + 1):
		listName.append(name + str(i))
	return listName
	
dataEnteringNode = IN

strWall = []
wallTypes = []

elements = FilteredElementCollector(doc).OfClass(Wall)

for i in elements:
	strWall.append(i.WallType.GetCompoundStructure().GetLayers())
	wallTypes.append(i.WallType)
	
TransactionManager.Instance.EnsureInTransaction(doc)
paramNanes = _Concat('00_Слой', 5)
for w in wallTypes:
	for pn in paramNanes:
		w.LookupParameter(pn).Set('')
TransactionManager.Instance.TransactionTaskDone()

listFinal_Mat = []
listFinal_Width = []

for s in strWall:
	listMat = []
	listWidth = []
	for l in s:
		listMat.append(doc.GetElement(l.MaterialId))
		listWidth.append((l.Width * 304.8).ToString())
	listFinal_Mat.append(listMat)
	listFinal_Width.append(listWidth)
OUT = listFinal_Mat,listFinal_Width,wallTypes
