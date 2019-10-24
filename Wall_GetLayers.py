import clr
clr.AddReference('RevitAPI')
from Autodesk.Revit.DB import *

clr.AddReference("RevitServices")
import RevitServices
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager

doc = DocumentManager.Instance.CurrentDBDocument

dataEnteringNode = IN

str = []
wallTypes = []

elements = FilteredElementCollector(doc).OfClass(Wall)

for i in elements:
	str.append(i.WallType.GetCompoundStructure().GetLayers())
	wallTypes.append(i.WallType)

listWidthFinalMat = []
listWidthFinalWidth = []

for s in str:
	listMat = []
	listWidth = []
	for l in s:
		listMat.append(doc.GetElement(l.MaterialId))
		listWidth.append(l.Width * 304.8)
	listWidthFinalMat.append(listMat)
	listWidthFinalWidth.append(listWidth)
OUT = listWidthFinalMat,listWidthFinalWidth,wallTypes
