import clr
clr.AddReference("RevitAPI")
from Autodesk.Revit.DB import ElementId, TemporaryViewMode
clr.AddReference("RevitServices")
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager
doc = DocumentManager.Instance.CurrentDBDocument


def doors_getAll(document):
    from Autodesk.Revit.DB import FilteredElementCollector, FamilyInstance, BuiltInCategory
    doors = FilteredElementCollector(document).OfClass(FamilyInstance).OfCategory(BuiltInCategory.OST_Doors)
    return doors.ToElements()


def doors_isMirrored(doors):
    from System.Collections.Generic import List
    elems = List[ElementId]()
    for door in doors:
        if door.Mirrored:
            elems.Add(door.Id)
    return elems


view = doc.ActiveView
m_doors = doors_isMirrored(doors_getAll(doc))

TransactionManager.Instance.EnsureInTransaction(doc)
mode = TemporaryViewMode.TemporaryHideIsolate
if m_doors:
    if view.IsInTemporaryViewMode(mode):
        view.DisableTemporaryViewMode(mode)
        view.IsolateElementsTemporary(m_doors)
    else:
        view.IsolateElementsTemporary(m_doors)
    OUT = [doc.GetElement(d) for d in m_doors]
else:
    if view.IsInTemporaryViewMode(mode):
        view.DisableTemporaryViewMode(mode)
    OUT = "Нет зеркальных дверей"
TransactionManager.Instance.TransactionTaskDone()
