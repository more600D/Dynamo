import clr
clr.AddReference("RevitAPI")
from Autodesk.Revit.DB import ElementId, ParameterType

clr.AddReference("RevitServices")
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager


def create_new_name(old_name):
    split = old_name.split("_")
    if split:
        return "_{}.{}".format(split[2], split[1])
    else:
        return old_name


def set_new_name(name):
    fm = doc.FamilyManager
    params = fm.GetParameters()
    mlist = []
    for i in params:
        old_name = i.Definition.Name
        if name in old_name:
            new_name = create_new_name(old_name)
            fm.RenameParameter(i, new_name)
            mlist.append(old_name)
            mlist.append(new_name)
        param_type = i.Definition.ParameterType
        if param_type == ParameterType.Material:
            fm.Set(i, ElementId(-1))
    return mlist


doc = DocumentManager.Instance.CurrentDBDocument
params = [UnwrapElement(i) for i in IN[1]]


TransactionManager.Instance.EnsureInTransaction(doc)

result = set_new_name("BOS")

TransactionManager.Instance.TransactionTaskDone()

OUT = result