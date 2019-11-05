import clr
clr.AddReference('RevitAPI')
import Autodesk
from Autodesk.Revit.DB import FilteredElementCollector, SharedParameterElement

clr.AddReference('RevitServices')
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager
doc = DocumentManager.Instance.CurrentDBDocument

import System


def GetParamByName(parameters, name):
    for p in parameters:
        if p.Name == name:
            return p


new_group = System.Enum.Parse(Autodesk.Revit.DB.BuiltInParameterGroup, IN[0])
params = FilteredElementCollector(doc).OfClass(SharedParameterElement)
param = GetParamByName(params, IN[1])

TransactionManager.Instance.EnsureInTransaction(doc)
if IN[2]:
    for i in params:
        i.GetDefinition().ParameterGroup = new_group
        OUT = 'Изменение группирования всем параметрам'
else:
    param.GetDefinition().ParameterGroup = new_group
    OUT = 'Изменение группирования для ' + param.Name
TransactionManager.Instance.TransactionTaskDone()
