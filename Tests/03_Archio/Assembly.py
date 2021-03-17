import clr
from System.Collections.Generic import List
clr.AddReference("RevitAPI")
from Autodesk.Revit.DB import AssemblyInstance, ElementId, \
    AssemblyViewUtils, XYZ, ViewOrientation3D, BuiltInCategory, BuiltInParameter, \
    SectionType, UnitUtils, DisplayUnitType, Viewport, FilteredElementCollector, \
    ScheduleHorizontalAlignment, ElementTransformUtils, View, ScheduleSheetInstance, \
    AssemblyDetailViewOrientation, Line, ReferenceArray, Options, IFamilyLoadOptions, FamilySource
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
        param = elem.Symbol.get_Parameter(BuiltInParameter.ALL_MODEL_MANUFACTURER)
        if param.AsString().lower() == self.name.lower():
            return True
        else:
            return False

    def AllowReference(self, ref, point):
        return True


def create_view_orientation3D(view3D):
    eyePosition = XYZ(-0.57648578469714, -32.18556060113, 6.27718419077313)
    upDirection = XYZ(0.220032087467546, 0.33175728167826, 0.917345620002694)
    forwardDirection = XYZ(-0.507032586085268, -0.764487372809919, 0.398091714887253)
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


# Dimensions----------------------------------------------------------------------------------
def create_dimension(element, point1, point2, reference_names_list, view, direction_to_move=XYZ(0, 0, 0)):
    line = Line.CreateBound(point1, point2)
    refArray = ReferenceArray()
    for ref in reference_names_list:
        refArray.Append(element.GetReferenceByName(ref))
    dim = doc.Create.NewDimension(view, line, refArray)
    ElementTransformUtils.MoveElement(doc, dim.Id, direction_to_move)
    return dim


def create_dimension_on_view(element, orientation, view, offset=0.2, document=doc):
    bb = element.get_BoundingBox(view)
    view_direction = view.ViewDirection.ToString()
    back = XYZ(0, 1, 0).ToString()
    front = XYZ(0, -1, 0).ToString()
    left = XYZ(-1, 0, 0).ToString()
    right = XYZ(1, 0, 0).ToString()
    top = XYZ(0, 0, 1).ToString()
    botton = XYZ(0, 0, -1).ToString()
    # Back or Front
    if view_direction == back or view_direction == front:
        if orientation == 'vertical':
            pt1 = XYZ(bb.Max.X, 0, bb.Min.Z)
            pt2 = XYZ(bb.Max.X, 0, bb.Max.Z)
            return create_dimension(element, pt1, pt2, ['3', '4'], view, XYZ(offset, 0, 0))
        elif orientation == 'horizontal':
            pt1 = XYZ(bb.Min.X, 0, bb.Min.Z)
            pt2 = XYZ(bb.Max.X, 0, bb.Min.Z)
            return create_dimension(element, pt1, pt2, ['1', '2'], view, XYZ(0, 0, -offset))
    # Left or Right
    elif view_direction == left or view_direction == right:
        if orientation == 'vertical':
            pt1 = XYZ(0, bb.Min.Y, bb.Max.Z)
            pt2 = XYZ(0, bb.Min.Y, bb.Min.Z)
            return create_dimension(element, pt1, pt2, ['3', '4'], view, XYZ(0, -offset, 0))
        elif orientation == 'horizontal':
            pt1 = XYZ(0, bb.Min.Y, bb.Min.Z)
            pt2 = XYZ(0, bb.Max.Y, bb.Min.Z)
            return create_dimension(element, pt1, pt2, ['5', '6'], view, XYZ(0, 0, -offset))
    # Top or Botton
    elif view_direction == top or view_direction == botton:
        if orientation == 'vertical':
            pt1 = XYZ(bb.Min.X, bb.Min.Y, 0)
            pt2 = XYZ(bb.Min.X, bb.Max.Y, 0)
            return create_dimension(element, pt1, pt2, ['5', '6'], view, XYZ(-offset, 0, 0))
        elif orientation == 'horizontal':
            pt1 = XYZ(bb.Min.X, bb.Min.Y, 0)
            pt2 = XYZ(bb.Max.X, bb.Min.Y, 0)
            return create_dimension(element, pt1, pt2, ['1', '2'], view, XYZ(0, -offset, 0))


# Family--------------------------------------------------------------------------------------
class FamilyOption(IFamilyLoadOptions):
    def OnFamilyFound(self, familyInUse, overwriteParameterValues):
        self.overwriteParameterValues = True
        return True

    def OnSharedFamilyFound(self, sharedFamily, familyInUse, source, overwriteParameterValues):
        self.source = FamilySource.Family
        self.overwriteParameterValues = True
        return True


def get_volume_from_bBox(element):
    bbox = element.get_BoundingBox(None)
    bbox_lenght = bbox.Max.X - bbox.Min.X
    bbox_width = bbox.Max.Y - bbox.Min.Y
    bbox_height = bbox.Max.Z - bbox.Min.Z
    return bbox_height * bbox_width * bbox_lenght


def get_square_from_solid(element):
    square = 0
    volume = 0
    solids = element.get_Geometry(Options())
    if solids:
        for solid in solids:
            volume += solid.Volume
            if hasattr(solid, 'Faces'):
                for face in solid.Faces:
                    mat_id = face.MaterialElementId
                    if mat_id.IntegerValue == -1:
                        square += face.Area
        return square, volume


def set_parameter_by_name(value, param_name, document):
    f_manager = document.FamilyManager
    if len(list(f_manager.Types)) == 0:
        f_manager.NewType('Тип 1')
    param = f_manager.get_Parameter(param_name)
    if param:
        if param.CanAssignFormula:
            val = UnitUtils.ConvertFromInternalUnits(value, param.DisplayUnitType)
            f_manager.SetFormula(param, str(val))
            return '{} - {}'.format(param_name, val)
    else:
        return 'Not OK'


# --------------------------------------------------------------------------------------------

try:
    sel = uidoc.Selection.PickObject(ObjectType.Element, CustomISelectionFilter('arhio'))
except Exception.message:
    TaskDialog.Show('Нет таких стен', 'Не выбраны стены')

elem = doc.GetElement(sel.ElementId)
elem_name = elem.LookupParameter('ARH_mk').AsString()
ids = List[ElementId]()
ids.Add(sel.ElementId)

TransactionManager.Instance.EnsureInTransaction(doc)
# Создание сборки
assembly = AssemblyInstance.Create(doc, ids, elem.Category.Id)

# Создание листа сборки
assembly_sheet = AssemblyViewUtils.CreateSheet(doc, assembly.Id, get_title_block('ARH_TitleBlock'))
assembly_sheet.Name = elem_name

# Создание 3д вида
view3D = create_View3D(assembly, 10)
pt_view3d = XYZ(1.12578803139851, 0.250911809407337, 0)
vp_view3d = Viewport.Create(doc, assembly_sheet.Id, view3D.Id, pt_view3d)
change_type(vp_view3d, 'ARH_БезЗаголовка')

# Создание спецификации
view_schedule = create_schedule(assembly)
view_schedule.ViewTemplateId = select_template_id('ARH_Detail_Template')
vp_schedule = ScheduleSheetInstance.Create(doc, assembly_sheet.Id, view_schedule.Id, XYZ.Zero)
doc.Regenerate()
move_element_schedule(vp_schedule, assembly_sheet, 415, 292)

# Создание разреза
pt_section_view = XYZ(1.10604515064852, 0.626337804965914, 0)
section_view = create_detail_section(assembly,
                                     AssemblyDetailViewOrientation.DetailSectionB,
                                     assembly_sheet,
                                     pt_section_view,
                                     'ARH_Заголовок',
                                     'ARH_Section')
title_on_sheet = section_view[0].get_Parameter(BuiltInParameter.VIEW_DESCRIPTION).Set('1-1')

# Создание фасада
pt_right_view = XYZ(0.491748513235149, 0.626337804965914, 0)
right_view = create_detail_section(assembly,
                                   AssemblyDetailViewOrientation.ElevationBack,
                                   assembly_sheet,
                                   pt_right_view,
                                   'ARH_БезЗаголовка',
                                   'ARH_Section')

# Создание вида сверху
pt_top_view = XYZ(0.491049476255798, 0.243470403613338, 0)
top_view = create_detail_section(assembly,
                                 AssemblyDetailViewOrientation.ElevationTop,
                                 assembly_sheet,
                                 pt_top_view,
                                 'ARH_БезЗаголовка',
                                 'ARH_Section')
center = top_view[1].GetBoxCenter()
ElementTransformUtils.MoveElement(doc, top_view[1].Id, pt_top_view - center)

TransactionManager.Instance.TransactionTaskDone()
TransactionManager.Instance.ForceCloseTransaction()

TransactionManager.Instance.EnsureInTransaction(doc)
assembly.AssemblyTypeName = elem_name
create_dimension_on_view(elem, 'horizontal', right_view[0])
create_dimension_on_view(elem, 'vertical', right_view[0])
create_dimension_on_view(elem, 'horizontal', right_view[0])
create_dimension_on_view(elem, 'vertical', right_view[0])
create_dimension_on_view(elem, 'horizontal', section_view[0])
create_dimension_on_view(elem, 'vertical', section_view[0])
create_dimension_on_view(elem, 'horizontal', top_view[0])
create_dimension_on_view(elem, 'vertical', top_view[0])
TransactionManager.Instance.TransactionTaskDone()

OUT = assembly
