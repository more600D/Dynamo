import clr
clr.AddReference("RevitAPI")
from Autodesk.Revit.DB import FilteredElementCollector
clr.AddReference("RevitServices")
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager


doc = DocumentManager.Instance.CurrentDBDocument
uiapp = DocumentManager.Instance.CurrentUIApplication
app = uiapp.Application

srd = app.OpenSharedParameterFile()
for group in srd.Groups:
    for ExDef in group.Definitions:
        if "ADSK_Зона" == ExDef.Name:
            OUT = ExDef

# OUT = [s.Definitions for s in srd.Groups]
