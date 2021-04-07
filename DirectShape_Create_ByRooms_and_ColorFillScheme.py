# -*- coding: utf-8 -*-
import clr
clr.AddReference("RevitAPI")
from Autodesk.Revit.DB import DirectShape, FilteredElementCollector, BuiltInCategory, \
    SpatialElementGeometryCalculator, ElementId, GeometryObject, DirectShapeType, DirectShapeLibrary, \
    BuiltInParameter, Transform, ViewFamilyType, View3D, ViewFamily, Category, OverrideGraphicSettings
clr.AddReference("RevitServices")
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager
from System.Collections.Generic import List

doc = DocumentManager.Instance.CurrentDBDocument
uiapp = DocumentManager.Instance.CurrentUIApplication
app = uiapp.Application


def get_overidegraphics(color):
    org = OverrideGraphicSettings()
    org.SetSurfaceBackgroundPatternVisible(False)
    org.SetSurfaceForegroundPatternColor(color)
    org.SetSurfaceForegroundPatternId(ElementId(3))
    return org


def get_color_from_colorscheme(view):
    cat = Category.GetCategory(doc, BuiltInCategory.OST_Rooms)
    color_scheme_id = view.GetColorFillSchemeId(cat.Id)  # Получение цветовой схемы
    colorfill_scheme = doc.GetElement(color_scheme_id)
    if colorfill_scheme:
        entries = colorfill_scheme.GetEntries()  # Получение всех элементов цветовой схемы
        data = {}
        for entry in entries:
            data[entry.GetStringValue()] = entry.Color
        return data


def create_view(doc, name):
    view_family_type_col = FilteredElementCollector(doc).OfClass(ViewFamilyType)
    view3d_col = FilteredElementCollector(doc).OfClass(View3D)
    view3d_names = [v.Name for v in view3d_col]
    for view_family_type in view_family_type_col:
        if view_family_type.ViewFamily == ViewFamily.ThreeDimensional:
            if name not in view3d_names:
                view3d = View3D.CreateIsometric(doc, view_family_type.Id)
                view3d.Name = name
                view3d.get_Parameter(BuiltInParameter.MODEL_GRAPHICS_STYLE).Set(3)
                for cat in doc.Settings.Categories:
                    if cat.Name != 'Generic Models' and view3d.CanCategoryBeHidden(cat.Id):
                        view3d.SetCategoryHidden(cat.Id, True)
                return view3d
            else:
                for view in view3d_col:
                    if view.Name == name:
                        return view


def get_directshape_type(name):
    types = FilteredElementCollector(doc).OfClass(DirectShapeType).ToElements()
    types_name = [t.FamilyName for t in types]
    if name not in types_name:
        ds_type = DirectShapeType.Create(doc, name, ElementId(BuiltInCategory.OST_GenericModel))
        ds_library = DirectShapeLibrary.GetDirectShapeLibrary(doc)
        ds_library.AddDefinitionType(name, ds_type.Id)
        return ds_type
    else:
        for ds_type in types:
            if name == ds_type.FamilyName:
                return ds_type


def delete_class_elements(class_name, document):
    elem_col = FilteredElementCollector(document).OfClass(class_name).ToElements()
    if elem_col:
        for element in elem_col:
            document.Delete(element.Id)


def create_directshape(room_collection, view_name):
    if room_collection:
        document = room_collection[0].Document
        delete_class_elements(DirectShape, document)
        delete_class_elements(DirectShapeType, document)
        datashape = []
        bad_rooms = []
        view = create_view(document, view_name)
        data_colors = get_color_from_colorscheme(document.ActiveView)
        if data_colors:
            for room in room_collection:
                try:
                    calculator = SpatialElementGeometryCalculator(document)
                    geometry_result = calculator.CalculateSpatialElementGeometry(room)
                    room_solid = geometry_result.GetGeometry()
                    geometry_objects = List[GeometryObject]()
                    geometry_objects.Add(room_solid)
                    room_name = room.get_Parameter(BuiltInParameter.ROOM_NAME).AsString()

                    ds_type = get_directshape_type(room_name)
                    ds = DirectShape.CreateElementInstance(document, ds_type.Id, \
                        ElementId(BuiltInCategory.OST_GenericModel), \
                        room_name, Transform.Identity)
                    ds.ApplicationId = uiapp.ActiveAddInId.ToString()
                    ds.ApplicationDataId = room.UniqueId
                    ds.SetTypeId(ds_type.Id)
                    ds.SetShape(geometry_objects)
                    view.SetElementOverrides(ds.Id, get_overidegraphics(data_colors[room_name]))
                    datashape.append(ds)
                except Exception:
                    bad_rooms.append(room)
            return room_collection
        else:
            return 'Перейдите на вид,\r\nгде применена цветовая схема'


room_col = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Rooms).ToElements()

TransactionManager.Instance.EnsureInTransaction(doc)
rooms = create_directshape(room_col, 'Rooms in 3D')
TransactionManager.Instance.TransactionTaskDone()

OUT = rooms
