import clr
clr.AddReference('RevitAPI')
from Autodesk.Revit.DB import FilteredElementCollector, BuiltInCategory, UnitUtils, DisplayUnitType
clr.AddReference('RevitServices')
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager

doc = DocumentManager.Instance.CurrentDBDocument

el = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_GenericModel) \
    .WhereElementIsNotElementType().ToElements()

el_filter = []
point_z = []

TransactionManager.Instance.EnsureInTransaction(doc)
for i in el:
    param_group_model = i.Symbol.LookupParameter('Группа модели')
    param_otmetka = i.LookupParameter(IN[1])  # noqa
    if param_group_model:
        if param_group_model.AsString() == IN[0]:  # noqa
            el_filter.append(i)
            pointXYZ = i.Location.Point
            point_z.append(round(UnitUtils.ConvertFromInternalUnits(pointXYZ.Z, DisplayUnitType.DUT_MILLIMETERS)))
    else:
        OUT = "Нет совпадающих критериев"
    if param_otmetka:
        for p in point_z:
            param_otmetka.Set(UnitUtils.ConvertToInternalUnits(p, param_otmetka.DisplayUnitType))
    else:
        OUT = 'Нет такого параметра для записи значения'
TransactionManager.Instance.TransactionTaskDone()
