import clr
clr.AddReference("RevitAPI")
clr.AddReference("RevitServices")
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager
doc = DocumentManager.Instance.CurrentDBDocument

floor_param_name = IN[1]
slab_param_name = IN[2]


def get_floors(doc, floor_param_name, slab_param_name):
    from Autodesk.Revit.DB import FilteredElementCollector, Floor, ElementClassFilter, HostedSweep
    all_floors = FilteredElementCollector(doc).OfClass(Floor).ToElements()
    result = []
    filter = ElementClassFilter(HostedSweep)
    for floor in all_floors:
        param = floor.LookupParameter(floor_param_name)
        if param:
            value = param.AsString()
            slabs = floor.GetDependentElements(filter)
            if slabs:
                for s in slabs:
                    elem = doc.GetElement(s)
                    slab_param = elem.LookupParameter(slab_param_name)
                    if slab_param:
                        slab_param.Set(value)
                        result.append(elem)
                    else:
                        result.append('There is no such slab parameter')
        else:
            return 'There is no such floor parameter'
    return result


TransactionManager.Instance.EnsureInTransaction(doc)
result = get_floors(doc, floor_param_name, slab_param_name)
TransactionManager.Instance.TransactionTaskDone()

OUT = result