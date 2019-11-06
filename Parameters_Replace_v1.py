import System
import clr
clr.AddReference('RevitAPI')
import Autodesk
from Autodesk.Revit.DB import FilteredElementCollector, FamilyManager
from Autodesk.Revit.ApplicationServices import ControlledApplication
clr.AddReference('RevitServices')
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager

doc = DocumentManager.Instance.CurrentDBDocument
uiapp = DocumentManager.Instance.CurrentUIApplication
app = uiapp.Application
fm = doc.FamilyManager


def GetByName(name):
    for p in fm.GetParameters():
        if p.Definition.Name == name:
            return p
def GetName(group_list, name):
    for g in group_list:
        if g.Name == name:
            return g


param = GetByName(IN[0])
group = System.Enum.Parse(Autodesk.Revit.DB.BuiltInParameterGroup, IN[3])
shared_params = app.OpenSharedParameterFile().Groups
names = GetName(shared_params, IN[1]).Definitions
param_names = GetName(names, IN[2])

if param.IsShared is True:
    OUT = 'Параметр общий'
elif GetName(shared_params, IN[1]) is None:
    OUT = 'Нет такой группы'
else:
    TransactionManager.Instance.EnsureInTransaction(doc)
    replace_param = doc.FamilyManager.ReplaceParameter(param, param_names, group, param.IsInstance)
    TransactionManager.Instance.TransactionTaskDone()
    OUT = 'Готово!'
