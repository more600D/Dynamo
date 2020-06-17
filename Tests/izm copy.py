import clr
clr.AddReference("RevitAPI")
from Autodesk.Revit.DB import FilteredElementCollector, BuiltInCategory
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


def SetParameter(el, param_name, count, value):
    param_number = el.LookupParameter("00_Изм{}_{}".format(count, param_name))
    if param_number:
        param_number.Set(value)


revision_col = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_GenericAnnotation). \
    WhereElementIsNotElementType().ToElements()
list_revisions = []
for revision in revision_col:
    family = doc.GetElement(revision.GetTypeId()).Family
    if '022_ОблакоИзменения' in family.Name:
        list_revisions.append(revision)
list_revisions = group_by_key(list_revisions, lambda x: x.OwnerViewId)

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
                        SetParameter(titleblock, 'Номер', i, '')
                        SetParameter(titleblock, 'Количество', i, 0)
                        SetParameter(titleblock, 'Тип', i, '')
                        SetParameter(titleblock, 'НомерРазрешения', i, '')
                        SetParameter(titleblock, 'Дата', i, '')
                SetParameter(titleblock, 'Номер', count, rev_number)
                SetParameter(titleblock, 'Количество', count, count_revision)
                SetParameter(titleblock, 'Тип', count, rev_type)
                SetParameter(titleblock, 'НомерРазрешения', count, rev_solution)
                SetParameter(titleblock, 'Дата', count, rev_date)
            count += 1
        for r in rev:
            sheet = doc.GetElement(r.OwnerViewId)
            param1 = sheet.LookupParameter('GP_Номер_листа')
            if param1:
                num1 = param1.AsInteger()
            param2 = sheet.LookupParameter('К_Ш.НомерЛиста')
            if param2:
                num2 = param2.AsString()
            if num2:
                sheet_num = '{}.{}'.format(num1, num2)
            else:
                sheet_num = str(num1)
            r.LookupParameter('О_ИЗМ_НомерЛиста').Set(sheet_num)
TransactionManager.Instance.TransactionTaskDone()

OUT = f_list
