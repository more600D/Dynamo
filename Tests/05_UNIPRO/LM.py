import clr
clr.AddReference("RevitAPI")
from Autodesk.Revit.DB import BuiltInParameter, ElementClassFilter, FamilyInstance

clr.AddReference("RevitServices")
from RevitServices.Transactions import TransactionManager


def get_dependent_elements(element):
    doc = element.Document
    class_filter = ElementClassFilter(FamilyInstance)
    depends = element.GetDependentElements(class_filter)
    depends_element_list = []
    for d in depends:
        elem = doc.GetElement(d)
        element_id = element.Id
        param = elem.get_Parameter(BuiltInParameter.ALL_MODEL_INSTANCE_COMMENTS).Set(str(element_id))
        depends_element_list.append(elem)
    return depends_element_list


elem = UnwrapElement(IN[1])  # noqa
TransactionManager.Instance.EnsureInTransaction(elem.Document)
result = get_dependent_elements(elem)
TransactionManager.Instance.TransactionTaskDone()
OUT = result