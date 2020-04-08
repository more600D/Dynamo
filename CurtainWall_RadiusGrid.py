import clr
clr.AddReference("RevitAPI")
from Autodesk.Revit.DB import UnitUtils, DisplayUnitType
clr.AddReference("RevitServices")
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager

doc = DocumentManager.Instance.CurrentDBDocument


def Convert_toMM(value):
    return UnitUtils.ConvertFromInternalUnits(value, DisplayUnitType.DUT_MILLIMETERS)


elem = UnwrapElement(IN[1])

if elem.CurtainGrid:
    curve = elem.Location.Curve
    if elem.Location.Curve.ToString() == 'Autodesk.Revit.DB.Arc':
        value = curve.Radius
        panelsIds = elem.CurtainGrid.GetPanelIds()
        panels = []
        TransactionManager.Instance.EnsureInTransaction(doc)
        for p in panelsIds:
            panel = doc.GetElement(p)
            param = panel.LookupParameter('ADSK_Размер_Радиус').Set(value)
            panels.append(panel)
        TransactionManager.Instance.TransactionTaskDone()
        OUT = Convert_toMM(value), panels
    else:
        OUT = 'Витраж прямой!'
else:
    OUT = 'Не выбран витраж!'
