import clr
clr.AddReference('RevitAPI')
from Autodesk.Revit.DB import *
import Autodesk

clr.AddReference("RevitServices")
import RevitServices
from RevitServices.Persistence import DocumentManager

DataEnteringNode = IN

LinkedFiles = IN[1]

Files = []
for i in LinkedFiles:
	Files.append(UnwrapElement(i))

docs = []

for inputdoc in Files:
	if inputdoc == None:
		doc = DocumentManager.Instance.CurrentDBDocument
	elif inputdoc.GetType().ToString() == "Autodesk.Revit.DB.RevitLinkInstance":
		doc = inputdoc.GetLinkDocument()
	elif inputdoc.GetType().ToString() == "Autodesk.Revit.DB.Document":
		doc = inputdoc
	else: doc = None
	docs.append(doc)
colWorkSets = []
for colWorkSet in docs:
	collector = FilteredWorksetCollector(colWorkSet).OfKind(WorksetKind.UserWorkset).ToWorksets()
	colWorkSets.append(collector)
workSetNames = []
workSetNameLink = []
for workSetName in colWorkSets:
	for i in workSetName:
		workSetNames.append(i.Name)

OUT = workSetNames
