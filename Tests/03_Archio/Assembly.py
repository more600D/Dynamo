import clr
import csv
from System.Collections.Generic import List
clr.AddReference("RevitAPI")
from Autodesk.Revit.DB import AssemblyInstance, ElementId, \
    AssemblyViewUtils, XYZ, ViewOrientation3D, BuiltInCategory, BuiltInParameter
clr.AddReference('RevitAPIUI')
from Autodesk.Revit.UI.Selection import ObjectType, Selection, ISelectionFilter
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


def add_field(schedule, name):
    definition = schedule.Definition
    all_fields = definition.GetSchedulableFields()
    for field in all_fields:
        if field.GetName(doc) == name:
            definition.AddField(field)
        else:
            return 'нет такого параметра'


name_detal = 'IZD-AK45-1'
try:
    sel = uidoc.Selection.PickObject(ObjectType.Element, CustomISelectionFilter(name_detal))
except Exception.message:
    TaskDialog.Show('Нет таких стен', 'Не выбраны стены')

elem = doc.GetElement(sel.ElementId)
ids = List[ElementId]()
ids.Add(sel.ElementId)

TransactionManager.Instance.EnsureInTransaction(doc)
try:
    assembly = AssemblyInstance.Create(doc, ids, elem.Category.Id)
    assembly.Name = name_detal
except Exception:
    pass
TransactionManager.Instance.TransactionTaskDone()
TransactionManager.Instance.ForceCloseTransaction()

TransactionManager.Instance.EnsureInTransaction(doc)

view3D = AssemblyViewUtils.Create3DOrthographic(doc, assembly.Id)
create_view_orientation3D(view3D)
view3D.Scale = 20

view_schedule = AssemblyViewUtils.CreateSingleCategorySchedule(doc, assembly.Id, elem.Category.Id)

TransactionManager.Instance.TransactionTaskDone()

# view_schedule = doc.GetElement(ElementId(314536))
definition = view_schedule.Definition
all_fields = definition.GetSchedulableFields()

TransactionManager.Instance.EnsureInTransaction(doc)

for f in definition.GetFieldOrder():
    definition.RemoveField(f)

add_field(view_schedule, 'ARH_sr')
add_field(view_schedule, 'ARH_v')

TransactionManager.Instance.TransactionTaskDone()


OUT = all_fields
