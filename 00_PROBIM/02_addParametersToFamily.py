import clr
clr.AddReference("RevitAPI")
from Autodesk.Revit.DB import FamilyManager
clr.AddReference("RevitServices")
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager
from System import Guid
doc = DocumentManager.Instance.CurrentDBDocument
uiapp = DocumentManager.Instance.CurrentUIApplication
app = uiapp.Application


def is_exist_parameter_by_guid(guid, family_manager):
    exists = False
    for param in family_manager.Parameters:
        if param.GuidValue == guid:
            exists = True
    return exists


def add_parameter(document, guid=0):
    if document.IsFamilyDocument:
        result = []
        from Autodesk.Revit.DB import Definitions, ExternalDefinitionCreationOptions, SpecTypeId
        guid = Guid("a8cdbf7b-d60a-485e-a520-447d2055f351")
        opt_ext_definition = ExternalDefinitionCreationOptions('ADSK_Завод-изготовитель', SpecTypeId.String.Text)
        opt_ext_definition.GUID = guid
        definition = Definitions().Create(opt_ext_definition)
        fam_manager = document.FamilyManager
        result.append(definition)
        return result




OUT = add_parameter(doc)
