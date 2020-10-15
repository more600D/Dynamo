import clr
clr.AddReference("RevitAPI")
from Autodesk.Revit.DB import FilteredElementCollector, BuiltInCategory, SpatialElementGeometryCalculator, \
    UnitUtils, DisplayUnitType, StorageType, BuiltInParameter
clr.AddReference("RevitServices")
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager

doc = DocumentManager.Instance.CurrentDBDocument
uiapp = DocumentManager.Instance.CurrentUIApplication
app = uiapp.Application

room_col = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Rooms)
calculator = SpatialElementGeometryCalculator(doc)

TransactionManager.Instance.EnsureInTransaction(doc)
report = []
for room in room_col:
    param = room.LookupParameter('Комментарии')
    room_name = room.get_Parameter(BuiltInParameter.ROOM_NAME).AsString()
    result = calculator.CalculateSpatialElementGeometry(room)
    room_solid = result.GetGeometry()
    for face in room_solid.Faces:
        faceNormal = face.FaceNormal
        if faceNormal.Z < 0:
            value = round(
                UnitUtils.ConvertFromInternalUnits(
                    face.Area,
                    DisplayUnitType.DUT_SQUARE_METERS),
                2)
            if param:
                if param.StorageType == StorageType.String:
                    param.Set(str(value))
                else:
                    param.Set(face.Area)
    report.append('{} - {}'.format(room_name, value))

TransactionManager.Instance.TransactionTaskDone()

OUT = report
