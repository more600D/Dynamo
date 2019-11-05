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


params = FilteredElementCollector(doc).OfClass(SharedParameterElement)
param = GetParamByName(params, IN[1])
params_definition = [i.GetDefinition() for i in params]
new_group = System.Enum.Parse(Autodesk.Revit.DB.BuiltInParameterGroup, IN[0])

TransactionManager.Instance.EnsureInTransaction(doc)
if IN[2] is False:
    for i in params_definition:
        i.ParameterGroup = new_group
else:
    param.GetDefinition().ParameterGroup = new_group
TransactionManager.Instance.TransactionTaskDone()

OUT = params_definition, new_group, param
