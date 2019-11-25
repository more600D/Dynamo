import clr
clr.AddReference('RevitAPI')
from Autodesk.Revit.DB import ViewSchedule

clr.AddReference('RevitServices')
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager

doc = DocumentManager.Instance.CurrentDBDocument


def getCategoryId():
    return doc.Settings.Categories.get_Item(IN[0]).Id  # noqa


def AddRegularFieldToSchedule(schedule, names):
    sch_definition = schedule.Definition
    fields = sch_definition.GetSchedulableFields()
    for i in fields:
        if i.GetName(doc) in names:
            sch_definition.AddField(i)


TransactionManager.Instance.EnsureInTransaction(doc)
a = ViewSchedule.CreateSchedule(doc, getCategoryId())
b = AddRegularFieldToSchedule(a, IN[1])  # noqa
TransactionManager.Instance.TransactionTaskDone()

OUT = getCategoryId(), b
