# -*- coding: utf-8 -*-
import clr
clr.AddReference("RevitAPI")
from Autodesk.Revit.DB import DirectShape, FilteredElementCollector, BuiltInCategory, \
    SpatialElementGeometryCalculator, ElementId, GeometryObject, DirectShapeType, DirectShapeLibrary, \
    BuiltInParameter, Transform
clr.AddReference("RevitServices")
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager
from System.Collections.Generic import List

doc = DocumentManager.Instance.CurrentDBDocument
uiapp = DocumentManager.Instance.CurrentUIApplication
app = uiapp.Application


def get_directshape_type(name):
    types = FilteredElementCollector(doc).OfClass(DirectShapeType).ToElements()
    types_name = [t.FamilyName for t in types]
    if name not in types_name:
        ds_type = DirectShapeType.Create(doc, name + '1', ElementId(BuiltInCategory.OST_GenericModel))
        ds_library = DirectShapeLibrary.GetDirectShapeLibrary(doc)
        ds_library.AddDefinitionType(name, ds_type.Id)
        return ds_type
    else:
        for ds_type in types:
            if name == ds_type.FamilyName:
                return ds_type


def create_directshape(room_collection):
    if room_collection:
        document = room_collection[0].Document
        direct_shapes_col = FilteredElementCollector(document).OfClass(DirectShape).ToElements()
        if direct_shapes_col:
            for shape in direct_shapes_col:
                document.Delete(shape.Id)
        datashape = []
        for room in room_collection:
            calculator = SpatialElementGeometryCalculator(document)
            geometry_result = calculator.CalculateSpatialElementGeometry(room)
            room_solid = geometry_result.GetGeometry()
            geometry_objects = List[GeometryObject]()
            geometry_objects.Add(room_solid)
            room_name = room.get_Parameter(BuiltInParameter.ROOM_NAME).AsString()

            ds_type = get_directshape_type(room_name)
            ds = DirectShape.CreateElementInstance(document,
                                                   ds_type.Id,
                                                   ElementId(BuiltInCategory.OST_GenericModel),
                                                   room_name,
                                                   Transform.Identity)
            ds.SetTypeId(ds_type.Id)
            ds.SetShape(geometry_objects)
            datashape.append(ds)
        return datashape


room_col = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Rooms).ToElements()

TransactionManager.Instance.EnsureInTransaction(doc)
datashape = create_directshape(room_col)
TransactionManager.Instance.TransactionTaskDone()

OUT = datashape
