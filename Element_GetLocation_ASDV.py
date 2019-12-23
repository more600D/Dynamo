import System
import clr
clr.AddReference("RevitAPI")
from Autodesk.Revit.DB import FilteredElementCollector, Family, FamilyInstance, UnitUtils, DisplayUnitType
from Autodesk.Revit.DB.ExtensibleStorage import Schema
clr.AddReference("RevitServices")
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager


doc = DocumentManager.Instance.CurrentDBDocument

el_fam = FilteredElementCollector(doc).OfClass(Family).ToElements()
el_inst = FilteredElementCollector(doc).OfClass(FamilyInstance).ToElements()
schemaGuid = System.Guid('3cd61681-a611-4a2f-b49c-ea8f0030807b')
sch = Schema.Lookup(schemaGuid)

fam_name = [f.Name for f in el_fam if f.GetEntity(sch).SchemaGUID == schemaGuid]

el = []
param_offset_guid = System.Guid('e4793a44-6050-45b3-843e-cfb49d9191c5')
param_guid = System.Guid('6ec2f9e9-3d50-4d75-a453-26ef4e6d1625')

TransactionManager.Instance.EnsureInTransaction(doc)
for e in el_inst:
    if e.Symbol.Family.Name in fam_name and e.get_Parameter(param_offset_guid):
        lev = UnitUtils.ConvertFromInternalUnits(e.Location.Point.Z, DisplayUnitType.DUT_MILLIMETERS)
        param = e.get_Parameter(param_offset_guid)
        param_value = UnitUtils.ConvertFromInternalUnits(param.AsDouble(), param.DisplayUnitType)
        if e.get_Parameter(param_guid):
            param_set = e.get_Parameter(param_guid)
            value = UnitUtils.ConvertToInternalUnits(lev + param_value, param_set.DisplayUnitType)
            param_set.Set(value)
        el.append(e)
TransactionManager.Instance.TransactionTaskDone()

OUT = el
