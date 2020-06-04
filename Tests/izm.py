import clr
clr.AddReference("RevitAPI")
from Autodesk.Revit.DB import FilteredElementCollector, BuiltInCategory, ViewSheet
clr.AddReference("RevitServices")
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager
from itertools import groupby
from System import Guid

doc = DocumentManager.Instance.CurrentDBDocument


def group_by_key(elems, keyfunc):
    sorted_group = []
    for key, group in groupby(sorted(elems, key=keyfunc), key=keyfunc):
        sorted_group.append(list(group))
    return sorted_group


def SetParameter(param_name, count, value):
    param_number = titleblock.LookupParameter("00_Изм{}_{}".format(count, param_name))
    if param_number:
        param_number.Set(value)


view_sheets = FilteredElementCollector(doc).OfClass(ViewSheet).ToElements()

list_revisions = []
for sheet in view_sheets:
    revisions = FilteredElementCollector(doc, sheet.Id).OfCategory(BuiltInCategory.OST_GenericAnnotation). \
        WhereElementIsNotElementType().ToElements()
    revision_on_list = []
    for revision in revisions:
        family = doc.GetElement(revision.GetTypeId()).Family
        if '022_ОблакоИзменения' in family.Name:
            revision_on_list.append(revision)
    list_revisions.append(revision_on_list)
    list_revisions = filter(None, list_revisions)

guid = Guid('9ff5d8e3-fc81-4d47-b629-a055922c80cb')
f_list = []
for rev in list_revisions:
    f = group_by_key(rev, lambda x: x.get_Parameter(guid).AsString())
    f_list.append(f)

TransactionManager.Instance.EnsureInTransaction(doc)

for rev_list in f_list:
    num_in_list = 4
    if len(rev_list) > num_in_list:
        rev_list = rev_list[len(rev_list) - num_in_list:]
    count = 1
    for rev in rev_list:
        count_revision = len(rev)
        rev_number = rev[0].LookupParameter("О_ИЗМ_Номер").AsString()
        rev_type = rev[0].LookupParameter("О_ИЗМ_Тип").AsString()
        rev_solution = rev[0].LookupParameter("О_ИЗМ_НомерРазрешения").AsString()
        rev_date = rev[0].LookupParameter("К_Ш.ДатаВыпуска").AsString()
        titleblocks = FilteredElementCollector(doc, rev[0].OwnerViewId). \
            OfCategory(BuiltInCategory.OST_TitleBlocks).ToElements()
        for titleblock in titleblocks:
            family = doc.GetElement(titleblock.GetTypeId()).Family
            if '020_Основная надпись' in family.Name:
                if len(rev_list) < num_in_list:
                    for i in range(num_in_list, len(rev_list), -1):
                        SetParameter('Номер', i, 0)
                        SetParameter('Количество', i, 0)
                        SetParameter('Тип', i, '')
                        SetParameter('НомерРазрешения', i, '')
                        SetParameter('Дата', i, '')
                SetParameter('Номер', count, float(rev_number))
                SetParameter('Количество', count, count_revision)
                SetParameter('Тип', count, rev_type)
                SetParameter('НомерРазрешения', count, rev_solution)
                SetParameter('Дата', count, rev_date)
            count += 1

TransactionManager.Instance.TransactionTaskDone()

OUT = f_list
