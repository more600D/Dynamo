__title__ = 'Mirrored Doors'
__author__ = 'Shvydko'
__doc__ = 'Looking for mirrored doors'
from System.Collections.Generic import List
from Autodesk.Revit.DB import ElementId, Transaction, TemporaryViewMode

doc = __revit__.ActiveUIDocument.Document


def doors_getAll(document):
    from Autodesk.Revit.DB import FilteredElementCollector, FamilyInstance, BuiltInCategory
    doors = FilteredElementCollector(document).OfClass(FamilyInstance).OfCategory(BuiltInCategory.OST_Doors)
    return doors.ToElements()


def doors_isMirrored(doors):
    return [door for door in doors if door.Mirrored]


def show_dialog(title, mess):
    from Autodesk.Revit.UI import TaskDialog
    TaskDialog.Show(title, mess)


view = doc.ActiveView
elems = List[ElementId]()
m_doors = doors_isMirrored(doors_getAll(doc))

if m_doors:
    for door in m_doors:
        elems.Add(door.Id)

t = Transaction(doc, 'Mirrored doors')
t.Start()
mode = TemporaryViewMode.TemporaryHideIsolate
if elems:
    if view.IsInTemporaryViewMode(mode):
        view.DisableTemporaryViewMode(mode)
        view.IsolateElementsTemporary(elems)
    else:
        view.IsolateElementsTemporary(elems)
else:
    if view.IsInTemporaryViewMode(mode):
        view.DisableTemporaryViewMode(mode)
    show_dialog('Mirrored Doors', 'There are no mirrored doors!')

t.Commit()
