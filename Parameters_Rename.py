import clr
clr.AddReference('RevitAPI')
from Autodesk.Revit.DB import FilteredElementCollector, SharedParameterElement, Definitions, \
    ExternalDefinitionCreationOptions
clr.AddReference("RevitServices")
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager


doc = DocumentManager.Instance.CurrentDBDocument
uiapp = DocumentManager.Instance.CurrentUIApplication
app = uiapp.Application

params_col = FilteredElementCollector(doc).OfClass(SharedParameterElement).ToElements()
adsk = params_col[1]
param_type = adsk.GetDefinition().ParameterType
srd_file = app.OpenSharedParameterFile()
group = srd_file.Groups.get_Item('Renaming')
if not group:
    group = srd_file.Groups.Create('Renaming')

old_name = adsk.Name.Split('_')
new_name = 'SHV_{}'.format(old_name[1])
definition = Definitions()
exDef = ExternalDefinitionCreationOptions(new_name, param_type)
exDef.GUID = adsk.GuidValue
# exDef.Description = 


# TransactionManager.Instance.EnsureInTransaction(doc)
# doc.Delete(adsk.Id)
# TransactionManager.Instance.TransactionTaskDone()

if not group.Definitions.Item[new_name]:
    nn = group.Definitions.Create(exDef)

# new_param = group.Definitions.Create()

OUT = group.Definitions.Item[new_name]
