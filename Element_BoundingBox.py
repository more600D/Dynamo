import clr
clr.AddReference("RevitAPI")
from Autodesk.Revit.DB import UnitUtils, DisplayUnitType, Transaction
clr.AddReference('RevitAPIUI')
from Autodesk.Revit.UI.Selection import ObjectType, Selection
clr.AddReference("RevitServices")
from RevitServices.Persistence import DocumentManager


doc = DocumentManager.Instance.CurrentDBDocument
uidoc = DocumentManager.Instance.CurrentUIDocument
uiapp = DocumentManager.Instance.CurrentUIApplication
app = uiapp.Application

t = Transaction(doc, 'Получаение бокса')
t.Start()

el_p = uidoc.Selection.PickObject(ObjectType.Element, 'Выбрать элемент')
el = doc.GetElement(el_p)

e = el.get_BoundingBox(doc.ActiveView)
e_min = e.Min.X
e_max = e.Max.X

dis = UnitUtils.ConvertFromInternalUnits(e_max - e_min, DisplayUnitType.DUT_MILLIMETERS)
t.Commit()

OUT = el, dis
