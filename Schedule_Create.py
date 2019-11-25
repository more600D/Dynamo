# -*- coding: utf-8 -*-
import clr
clr.AddReference('RevitAPI')
from Autodesk.Revit.DB import ViewSchedule, Transaction

clr.AddReference('RevitServices')
from RevitServices.Persistence import DocumentManager

doc = DocumentManager.Instance.CurrentDBDocument
uiapp = DocumentManager.Instance.CurrentUIApplication
app = uiapp.Application


def getCategoryId():
    return doc.Settings.Categories.get_Item(IN[0]).Id  # noqa


def AddRegularFieldToSchedule(schedule, document, names):
    sch_definition = schedule.Definition
    fields = sch_definition.GetSchedulableFields()
    for i in fields:
        if i.GetName(document) in names:
            sch_definition.AddField(i)


docs = []
for i in app.Documents:
    if not i.IsFamilyDocument and not i.IsLinked:
        docs.append(i)

comment = "Создание спецификации " + IN[0]  # noqa
for d in docs:
    t = Transaction(d, comment)
    t.Start()
    a = ViewSchedule.CreateSchedule(d, getCategoryId())
    b = AddRegularFieldToSchedule(a, d, IN[1])  # noqa
    t.Commit()

OUT = [d.Title for d in docs], comment
