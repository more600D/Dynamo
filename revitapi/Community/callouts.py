import clr
clr.AddReference("RevitAPI")
import Autodesk.Revit.DB as DB
clr.AddReference("RevitServices")
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager


doc = DocumentManager.Instance.CurrentDBDocument

views = IN[0]
elems = []
for v in views:
    elems.append(UnwrapElement(v))

res = []
for el in elems:
    dep_element_ids = el.GetDependentElements(DB.ElementClassFilter(DB.Viewport))
    res.append(el.GetPrimaryViewId())


OUT = res
