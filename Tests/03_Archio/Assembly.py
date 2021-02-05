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
    def __init__(self, doc):
        self.doc = doc

    def AllowElement(self, elem):
        if elem.Category.Id.IntegerValue == BuiltInCategory.OST_Walls.value__:
            elem_type = doc.GetElement(elem.GetTypeId())
            width = elem_type.get_Parameter(BuiltInParameter.WALL_ATTR_WIDTH_PARAM).AsDouble()
            if width == 0.951443569553806:
                return True
        else:
            return False
    
    def AllowReference(self, ref, point):
        return True


def get_unwrap_element(data):
    """Unwrap element or elements.
    \nAlso check item if is it assembly"""
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

# sel = IN[1]  # noqa

# selected = get_unwrap_element(sel)
# ids = List[ElementId]()
# ids.Add(selected.Id)

# TransactionManager.Instance.EnsureInTransaction(doc)
# try:
#     assembly = AssemblyInstance.Create(doc, ids, selected.Category.Id)
#     assembly.Name = 'test_{}'.format(selected.Id)
# except Exception:
#     pass
# TransactionManager.Instance.TransactionTaskDone()
# TransactionManager.Instance.ForceCloseTransaction()

# TransactionManager.Instance.EnsureInTransaction(doc)

# view3D = AssemblyViewUtils.Create3DOrthographic(doc, assembly.Id)
# create_view_orientation3D(view3D)

# TransactionManager.Instance.TransactionTaskDone()


# try:
#     elem = uidoc.Selection.PickObject(ObjectType.Element,
#                                       CustomISelectionFilter(doc),
#                                       'Select elements')
# except Exception.message:
#     TaskDialog.Show('Нет таких стен', 'Не выбраны стены')

id_elem = ElementId(308886)
elem = doc.GetElement(id_elem)
elem_type = doc.GetElement(elem.GetTypeId())
width = elem_type.get_Parameter(BuiltInParameter.WALL_ATTR_WIDTH_PARAM).AsDouble()

OUT = width
