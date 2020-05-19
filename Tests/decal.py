import clr
clr.AddReference("RevitAPI")
from Autodesk.Revit.DB import FilteredElementCollector, BuiltInParameter
clr.AddReference("RevitServices")
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager


doc = DocumentManager.Instance.CurrentDBDocument
uiapp = DocumentManager.Instance.CurrentUIApplication
app = uiapp.Application

el = UnwrapElement(IN[0])  # noqa

decal_type = doc.GetElement(el.GetTypeId())
dacal_attributes = decal_type.get_Parameter(BuiltInParameter.DECAL_ATTRIBUTES)

OUT = decal_type.AppearanceAssetId
