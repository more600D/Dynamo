import clr
from System.Collections.Generic import List
clr.AddReference("RevitAPI")
from Autodesk.Revit.DB import AssemblyInstance, ElementId, \
    AssemblyViewUtils, XYZ, ViewOrientation3D, BuiltInCategory, BuiltInParameter, \
    SectionType, UnitUtils, DisplayUnitType, Viewport, FilteredElementCollector, \
    ScheduleHorizontalAlignment, ElementTransformUtils, View, ScheduleSheetInstance, \
    AssemblyDetailViewOrientation, ViewportRotation
clr.AddReference('RevitAPIUI')
from Autodesk.Revit.UI.Selection import ObjectType, ISelectionFilter
from Autodesk.Revit.UI import TaskDialog

clr.AddReference("RevitServices")
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager

doc = DocumentManager.Instance.CurrentDBDocument
uidoc = DocumentManager.Instance.CurrentUIApplication.ActiveUIDocument
# --------------------------------------------------------------------------------------------


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


def create_detail_section(assembly, orientation, sheet, point, vp_type_name=None, template=None, scale=5):
    section_view = AssemblyViewUtils.CreateDetailSection(doc, assembly.Id, orientation)
    section_view.Scale = scale
    vp_section_view = Viewport.Create(doc, sheet.Id, section_view.Id, point)
    if vp_type_name:
        change_type(vp_section_view, vp_type_name)
    if template:
        section_view.ViewTemplateId = select_template_id(template)
    return section_view, vp_section_view


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


def move_element(view_port, view, value_x, value_y):
    bb_vp = view_port.get_BoundingBox(view)
    if bb_vp:
        x = UnitUtils.ConvertToInternalUnits(value_x, DisplayUnitType.DUT_MILLIMETERS)
        y = UnitUtils.ConvertToInternalUnits(value_y, DisplayUnitType.DUT_MILLIMETERS)
        new_x = x - (bb_vp.Max.X - bb_vp.Min.X) / 2
        new_y = y + (bb_vp.Max.Y - bb_vp.Min.Y) / 2
        pt3 = XYZ(new_x, new_y, 0)
        point = ElementTransformUtils.MoveElement(doc, view_port.Id, pt3)
        return point


def move_element_schedule(scheduleview_port, view, value_x, value_y):
    bb_vp = scheduleview_port.get_BoundingBox(view)
    if bb_vp:
        x = UnitUtils.ConvertToInternalUnits(value_x, DisplayUnitType.DUT_MILLIMETERS)
        y = UnitUtils.ConvertToInternalUnits(value_y, DisplayUnitType.DUT_MILLIMETERS)
        new_x = x - bb_vp.Max.X - bb_vp.Min.X
        pt3 = XYZ(new_x, y, 0)
        point = ElementTransformUtils.MoveElement(doc, scheduleview_port.Id, pt3)
        return point


def select_template_id(name):
    col = FilteredElementCollector(doc).OfClass(View).ToElements()
    for tp in col:
        if tp.IsTemplate:
            if tp.Name == name:
                return tp.Id


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
# Создание сборки
assembly = AssemblyInstance.Create(doc, ids, elem.Category.Id)

# Создание листа сборки
assembly_sheet = AssemblyViewUtils.CreateSheet(doc, assembly.Id, get_title_block('ARH_TitleBlock'))
assembly_sheet.Name = elem.Name

# Создание 3д вида
view3D = create_View3D(assembly, 10)
vp_view3d = Viewport.Create(doc, assembly_sheet.Id, view3D.Id, XYZ.Zero)
change_type(vp_view3d, 'No Title')
move_element(vp_view3d, assembly_sheet, 410, 20)

# Создание спецификации
view_schedule = create_schedule(assembly)
view_schedule.ViewTemplateId = select_template_id('Detail_Template')
vp_schedule = ScheduleSheetInstance.Create(doc, assembly_sheet.Id, view_schedule.Id, XYZ.Zero)
doc.Regenerate()
move_element_schedule(vp_schedule, assembly_sheet, 415, 292)

# Создание разреза
pt_section_view = XYZ(1.10604515064852, 0.626337804965914, 0)
section_view = create_detail_section(assembly,
                                     AssemblyDetailViewOrientation.DetailSectionA,
                                     assembly_sheet,
                                     pt_section_view,
                                     'Title No Line',
                                     'ARH_Section')
title_on_sheet = section_view[0].get_Parameter(BuiltInParameter.VIEW_DESCRIPTION).Set('1-1')

# Создание фасада
pt_right_view = XYZ(0.457935776376508, 0.626337804965913, 0)
right_view = create_detail_section(assembly,
                                   AssemblyDetailViewOrientation.ElevationRight,
                                   assembly_sheet,
                                   pt_right_view,
                                   'No Title',
                                   'ARH_Section')

# Создание вида сверху
pt_top_view = XYZ(0.378418462541723, 0.255355082500111, 0)
top_view = create_detail_section(assembly,
                                 AssemblyDetailViewOrientation.ElevationTop,
                                 assembly_sheet,
                                 pt_top_view,
                                 'No Title',
                                 'ARH_Section')
top_view[1].Rotation = ViewportRotation.Clockwise
center = top_view[1].GetBoxCenter()
ElementTransformUtils.MoveElement(doc, top_view[1].Id, pt_top_view - center)

TransactionManager.Instance.TransactionTaskDone()
TransactionManager.Instance.ForceCloseTransaction()

TransactionManager.Instance.EnsureInTransaction(doc)
assembly.AssemblyTypeName = elem.Name
TransactionManager.Instance.TransactionTaskDone()

OUT = assembly
