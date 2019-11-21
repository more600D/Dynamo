import clr
clr.AddReference('RevitAPI')
from Autodesk.Revit.ApplicationServices import Application
from Autodesk.Revit.DB import Document
clr.AddReference('RevitServices')
from RevitServices.Persistence import DocumentManager


doc = DocumentManager.Instance.CurrentDBDocument
uiapp = DocumentManager.Instance.CurrentUIApplication
app = uiapp.Application


OUT = [i.Title for i in app.Documents]