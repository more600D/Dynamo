# -*- coding: utf-8 -*-
import clr
clr.AddReference('RevitAPI')
from Autodesk.Revit.DB import FilteredWorksetCollector, WorksetKind, Workset
clr.AddReference("RevitServices")
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager

uiapp = DocumentManager.Instance.CurrentUIApplication
app = uiapp.Application
doc = DocumentManager.Instance.CurrentDBDocument

file_path = IN[1]  # noqa

col = FilteredWorksetCollector(doc).OfKind(WorksetKind.UserWorkset).ToWorksets()

name_list = []
for c in col:
    name_list.append(c.Name)

if file_path.endswith('.rvt'):
    input_doc = app.OpenDocumentFile(file_path)
    if input_doc.GetType().ToString() == "Autodesk.Revit.DB.Document":
        report = 'None'
        if input_doc.IsWorkshared:
            input_col = FilteredWorksetCollector(input_doc).OfKind(WorksetKind.UserWorkset).ToWorksets()
            if not doc.IsWorkshared:
                if doc.CanEnableWorksharing():
                    doc.EnableWorksharing("Общие уровни и сетки", "Рабочий набор1")
            created_worksets = []
            TransactionManager.Instance.EnsureInTransaction(doc)
            for workset in input_col:
                workset_name = workset.Name
                if workset_name not in name_list:
                    created_worksets.append(workset_name)
                    try:
                        Workset.Create(doc, workset_name)
                    except Exception:
                        pass
                if len(created_worksets) > 0:
                    report = ["Создано {} набора(ов)".format(len(created_worksets)), created_worksets]
                else:
                    report = "Создано 0 рабочих наборов"
            TransactionManager.Instance.TransactionTaskDone()
        else:
            report = "Файл \"{}.rvt\" не является общим".format(input_doc.Title)
    input_doc.Close(False)
    OUT = report
