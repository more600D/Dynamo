import clr
from System.Collections.Generic import List
clr.AddReference("RevitAPI")
from Autodesk.Revit.DB import AssemblyInstance, ElementId, \
    AssemblyViewUtils, XYZ, ViewOrientation3D, BuiltInCategory, BuiltInParameter, \
    SectionType, UnitUtils, DisplayUnitType, Viewport, FilteredElementCollector, \
    ScheduleHorizontalAlignment, Options
clr.AddReference('RevitAPIUI')
from Autodesk.Revit.UI.Selection import ObjectType, ISelectionFilter
from Autodesk.Revit.UI import TaskDialog

clr.AddReference("RevitServices")
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager


doc = DocumentManager.Instance.CurrentDBDocument
uidoc = DocumentManager.Instance.CurrentUIApplication.ActiveUIDocument


class CustomISelectionFilter(ISelectionFilter):
    def __init__(self, name):
        self.name = name

    def AllowElement(self, elem):
        if elem.Symbol.FamilyName == self.name:
            return True
        else:
            return False

    def AllowReference(self, ref, point):
        return True


def get_unwrap_element(data):
    if not isinstance(data, list):
        elem = UnwrapElement(data)  # noqa
        if elem.Category.Name != 'Assemblies':
            return elem
        else:
            return 'Выберите не сборку'
    else:
        return [UnwrapElement(i) for i in data]  # noqa


def create_view_orientation3D(view3D):
    eyePosition = XYZ(-23.859921761, 14.537813974, 12.796544147)
    upDirection = XYZ(0.408248290, -0.408248290, 0.816496581)
    forwardDirection = XYZ(-0.577350269, 0.577350269, 0.577350269)
    orientation = ViewOrientation3D(eyePosition, upDirection, forwardDirection)
    view3D.SetOrientation(orientation)


def create_View3D(assembly, scale=7):
    view3D = AssemblyViewUtils.Create3DOrthographic(doc, assembly.Id)
    create_view_orientation3D(view3D)
    view3D.Scale = scale
    return view3D


def add_field(schedule, name, header):
    definition = schedule.Definition
    all_fields = definition.GetSchedulableFields()
    for field in all_fields:
        if field.GetName(doc) == name:
            f = definition.AddField(field)
            f.ColumnHeading = header
            f.HorizontalAlignment = ScheduleHorizontalAlignment.Center
        # else:
        #     return 'нет такого параметра'


def change_width_colomn(schedule, value=30):
    table_data_section = schedule.GetTableData().GetSectionData(SectionType.Body)
    table_data_section.RefreshData()
    definition = schedule.Definition
    for i in range(0, len(definition.GetFieldOrder())):
        table_data_section.SetColumnWidth(i, UnitUtils.ConvertToInternalUnits(value, DisplayUnitType.DUT_MILLIMETERS))


def create_schedule(assembly, headers=True, title=False):
    elem_id = list(assembly.GetMemberIds())[0]
    cat = doc.GetElement(elem_id).Category.Id
    view_schedule = AssemblyViewUtils.CreateSingleCategorySchedule(doc, assembly.Id, cat)
    definition = view_schedule.Definition
    definition.ClearFields()
    definition.ShowHeaders = headers
    definition.ShowTitle = title
    return view_schedule


def get_title_block(name):
    col = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_TitleBlocks).WhereElementIsElementType()
    for f in col:
        if f.Family.Name == name:
            return f.Id


def change_type(el, name):
    for type_id in el.GetValidTypes():
        elem_type = doc.GetElement(type_id)
        type_name = elem_type.get_Parameter(BuiltInParameter.ALL_MODEL_TYPE_NAME).AsString()
        if type_name == name:
            el.ChangeTypeId(type_id)


# --------------------------------------------------------------------------------------------
name_detal = 'IZD-AK45-1'
try:
    sel = uidoc.Selection.PickObject(ObjectType.Element, CustomISelectionFilter(name_detal))
except Exception.message:
    TaskDialog.Show('Нет таких стен', 'Не выбраны стены')

elem = doc.GetElement(sel.ElementId)
ids = List[ElementId]()
ids.Add(sel.ElementId)


TransactionManager.Instance.EnsureInTransaction(doc)

assembly = AssemblyInstance.Create(doc, ids, elem.Category.Id)

view3D = create_View3D(assembly)
view_schedule = create_schedule(assembly)
add_field(view_schedule, 'ARH_sr', 'Площадь разв. (S, м2)')
add_field(view_schedule, 'ARH_v', 'Объем (V, м3)')

assembly_sheet = AssemblyViewUtils.CreateSheet(doc, assembly.Id, get_title_block('ARH_TitleBlock'))
vp = Viewport.Create(doc, assembly_sheet.Id, view3D.Id, XYZ.Zero)
change_type(vp, 'No Title')
viewport_boundingbox = vp.get_BoundingBox(assembly_sheet)
doc.Regenerate()

TransactionManager.Instance.TransactionTaskDone()
TransactionManager.Instance.ForceCloseTransaction()

TransactionManager.Instance.EnsureInTransaction(doc)
change_width_colomn(view_schedule, 60)
assembly.AssemblyTypeName = elem.Name
assembly_sheet.Name = elem.Name
TransactionManager.Instance.TransactionTaskDone()

OUT = viewport_boundingbox
