import clr
clr.AddReference("RevitAPI")
from Autodesk.Revit.DB import FilteredElementCollector, Level, UnitUtils, DisplayUnitType, BuiltInParameter

clr.AddReference("RevitServices")
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager

doc = DocumentManager.Instance.CurrentDBDocument


def renameLevel(levels, sign=True):
    count = 1
    TransactionManager.Instance.EnsureInTransaction(doc)
    for ld in levels:
        elev_mm = UnitUtils.ConvertFromInternalUnits(ld.Elevation, DisplayUnitType.DUT_METERS)
        param = ld.get_Parameter(BuiltInParameter.DATUM_TEXT)
        if param:
            if sign:
                name_level = "L{}(+{:.3f})".format(count, elev_mm)
            else:
                name_level = "B{}({:.3f})".format(count, elev_mm)
            param.Set(name_level)
            count += 1
    TransactionManager.Instance.TransactionTaskDone()


level_col = FilteredElementCollector(doc).OfClass(Level).ToElements()

sorted_levels = sorted(level_col, key=lambda x: x.Elevation)

levels_up = []
levels_down = []

for l in sorted_levels:
    if l.Elevation >= 0:
        levels_up.append(l)
    else:
        levels_down.append(l)

renameLevel(levels_up)
renameLevel(reversed(levels_down), False)

OUT = levels_up, levels_down
