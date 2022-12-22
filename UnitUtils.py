import clr
clr.AddReference("RevitAPI")
from Autodesk.Revit.DB import UnitUtils
clr.AddReference("RevitServices")
from RevitServices.Persistence import DocumentManager

doc = DocumentManager.Instance.CurrentDBDocument


def round_square(room_area, round_number=2):
    version = int(doc.Application.VersionNumber)
    if version > 2021:
        from Autodesk.Revit.DB import UnitTypeId
        dut = UnitTypeId.SquareMeters
        value = round(UnitUtils.ConvertFromInternalUnits(room_area, dut), round_number)
        return UnitUtils.ConvertToInternalUnits(value, dut)
    else:
        from Autodesk.Revit.DB import DisplayUnitType
        dut = DisplayUnitType.DUT_SQUARE_METERS
        value = round(UnitUtils.ConvertFromInternalUnits(room_area, dut), round_number)
        return UnitUtils.ConvertToInternalUnits(value, dut)

room = UnwrapElement((IN[1]))  # noqa

OUT = round_square(room.Area)
