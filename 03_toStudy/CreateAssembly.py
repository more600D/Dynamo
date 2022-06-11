# -*- coding: utf-8 -*-
import clr
from System.Collections.Generic import List
clr.AddReference("RevitAPI")
from Autodesk.Revit.DB import Category, ElementId, AssemblyInstance
clr.AddReference("RevitServices")
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager


doc = DocumentManager.Instance.CurrentDBDocument


elem = UnwrapElement(IN[1])  # noqa
cat_id = elem.Category.Id
elem_id = List[ElementId]()
elem_id.Add(elem.Id)
sub_comp_ids = List[ElementId](elem.GetSubComponentIds())

TransactionManager.Instance.EnsureInTransaction(doc)
assembly = AssemblyInstance.Create(doc, elem_id, cat_id)
assembly.AddMemberIds(sub_comp_ids)
TransactionManager.Instance.TransactionTaskDone()

OUT = assembly