# -*- coding: utf-8 -*-
import clr
clr.AddReference("RevitServices")
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager

doc = DocumentManager.Instance.CurrentDBDocument

elems = UnwrapElement(IN[1])  # noqa
param_name = IN[2]  # noqa
data = IN[3]  # noqa
mirrored = []

TransactionManager.Instance.EnsureInTransaction(doc)

for el in elems:
    param = el.LookupParameter(param_name)
    if el.Mirrored and param:
        mirrored.append(el)
        param.Set(data)
    elif param:
        param.Set("")

TransactionManager.Instance.TransactionTaskDone()

OUT = len(elems)
