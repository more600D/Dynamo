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
for e in el_inst:
    if e.Symbol.Family.Name in fam_name:
        lev = UnitUtils.ConvertFromInternalUnits(e.Location.Point.Z, DisplayUnitType.DUT_MILLIMETERS)
        param = e.LookupParameter('00_Смещение.отУровня')
        param_value = UnitUtils.ConvertFromInternalUnits(param.AsDouble(), param.DisplayUnitType)
        if e.LookupParameter('ADSK_Отверстие_Отметка от нуля'):
            param_set = e.LookupParameter('ADSK_Отверстие_Отметка от нуля')
            value = UnitUtils.ConvertToInternalUnits(lev + param_value, param_set.DisplayUnitType)
            TransactionManager.Instance.EnsureInTransaction(doc)
            param_set.Set(value)
            TransactionManager.Instance.TransactionTaskDone()
        el.append(e)

OUT = el
