import clr
clr.AddReference("RevitAPI")
from Autodesk.Revit.DB import FilteredElementCollector, CurveElement, BuiltInCategory, UnitUtils, DisplayUnitType, \
    View, ViewType, GraphicsStyleType, Color, BuiltInParameterGroup, ParameterType
clr.AddReference("RevitServices")
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager


doc = DocumentManager.Instance.CurrentDBDocument


views = FilteredElementCollector(doc).OfClass(View)

line_length = 0
TransactionManager.Instance.EnsureInTransaction(doc)

for v in views:
    if v.ViewType == ViewType.FloorPlan:
        scale = v.Scale
        elems = FilteredElementCollector(doc, v.Id).OfClass(CurveElement)
        for e in elems:
            graphics_style_cat = e.LineStyle.GraphicsStyleCategory
            id_cat = graphics_style_cat.Id
            if BuiltInCategory(id_cat.IntegerValue) == BuiltInCategory.OST_ProfileFamilies:
                cat = graphics_style_cat
                line_length += e.GeometryCurve.Length

gs = cat.GetGraphicsStyle(GraphicsStyleType.Projection)
gsCat = gs.GraphicsStyleCategory
gsCat.LineColor = Color(IN[1].Red, IN[1].Green, IN[1].Blue)  # noqa
v.Scale = 1
v.Scale = scale

line_length = UnitUtils.ConvertFromInternalUnits(line_length, DisplayUnitType.DUT_MILLIMETERS)

f_manager = doc.FamilyManager
param_name = "_Профиль.Длина"
length_param = f_manager.get_Parameter(param_name)

if len(list(f_manager.Types)) == 0:
    f_manager.NewType('Тип 1')

if length_param:
    if length_param.CanAssignFormula:
        f_manager.SetFormula(length_param, str(line_length))
        OUT = "Длина профиля {}".format(round(line_length))
else:
    fparameter = f_manager.AddParameter(
        param_name, BuiltInParameterGroup.PG_DATA, ParameterType.Length, False)
    f_manager.SetFormula(fparameter, str(line_length))
    OUT = "Создался параметр \"{}\".\nДлина профиля {}".format(param_name, line_length)

TransactionManager.Instance.TransactionTaskDone()
