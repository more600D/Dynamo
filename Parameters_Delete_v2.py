# -*- coding: utf-8 -*-
import sys
pyt_path = r'C:\Program Files (x86)\IronPython 2.7\Lib'
sys.path.append(pyt_path)
import os
from System.IO import Directory
import clr
clr.AddReference('RevitAPI')
from Autodesk.Revit.DB import SaveAsOptions
clr.AddReference("RevitServices")
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager

uiapp = DocumentManager.Instance.CurrentUIApplication
app = uiapp.Application

optS = SaveAsOptions()
optS.OverwriteExistingFile = True
optS.Compact = True
optS.MaximumBackups = 1

need_params = IN[1]  # noqa
dir_path = IN[2]  # noqa

need_params = need_params.replace(', ', ',').split(',')
report = []

if Directory.Exists(dir_path):
    files = os.listdir(dir_path)
    files_rfa_path = filter(lambda x: x.endswith('.rfa'), files)
    families_path = []
    for f in files_rfa_path:
        if "000" not in f:
            families_path.append(f)

    for path in families_path:
        filepath = os.path.join(dir_path, path)
        family_doc = app.OpenDocumentFile(filepath)

        TransactionManager.Instance.EnsureInTransaction(family_doc)

        familyManager = family_doc.FamilyManager
        mlist = []
        mlist.append(family_doc.Title)
        for f_param in familyManager.Parameters:
            f_param_name = f_param.Definition.Name
            if f_param_name:
                if need_params:
                    for param in need_params:
                        if f_param_name == param:
                            try:
                                mlist.append('Параметр \"{}\" удален!'.format(f_param_name))
                                familyManager.RemoveParameter(f_param)
                            except Exception:
                                pass
        report.append(mlist)

        TransactionManager.Instance.ForceCloseTransaction()

        family_doc.SaveAs(filepath, optS)
        family_doc.Close(False)

OUT = report
