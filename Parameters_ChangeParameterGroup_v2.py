# -*- coding: utf-8 -*-
import sys
pyt_path = r'C:\Program Files (x86)\IronPython 2.7\Lib'
sys.path.append(pyt_path)
import os
import clr
import System
from System.IO import Directory
clr.AddReference('RevitAPI')
from Autodesk.Revit.DB import BuiltInParameterGroup, SaveAsOptions, Transaction
clr.AddReference("RevitServices")
from RevitServices.Persistence import DocumentManager

uiapp = DocumentManager.Instance.CurrentUIApplication
app = uiapp.Application


def parse_to_builtInParameterGroup(item):
    parse_item = System.Enum.Parse(
        BuiltInParameterGroup, item
    )
    return parse_item


def GetSharedParameter(name):
    srd = app.OpenSharedParameterFile()
    for group in srd.Groups:
        for ExDef in group.Definitions:
            if name == ExDef.Name:
                return ExDef


def MoveParameterToGroup(doc, fparam, toGroup, name):
    isInstance = fparam.IsInstance
    defination = fparam.Definition
    eDef = GetSharedParameter(defination.Name)
    fparam = doc.FamilyManager.ReplaceParameter(fparam, name, toGroup, isInstance)
    doc.FamilyManager.ReplaceParameter(fparam, eDef, toGroup, isInstance)


need_params = IN[1]  # noqa
param_groups = IN[2]  # noqa
dir_path = IN[3]  # noqa

if Directory.Exists(dir_path):
    files = os.listdir(dir_path)
    files_rfa_path = filter(lambda x: x.endswith('.rfa'), files)
    families_path = []
    for f in files_rfa_path:
        if "000" not in f:
            families_path.append(f)

    report = []

    for path in families_path:
        filepath = os.path.join(dir_path, path)
        family_doc = app.OpenDocumentFile(filepath)
        paramList = [i for i in family_doc.FamilyManager.Parameters]

        filtered_params = []

        for np in need_params:
            for p in paramList:
                if p.Definition.Name == np:
                    filtered_params.append(p)

        if filtered_params:
            trans = Transaction(family_doc, 'ChangeGroup')
            trans.Start()
            fam_report = []
            fam_report.append(family_doc.Title)

            for i in range(len(filtered_params)):
                parse_pg = parse_to_builtInParameterGroup(param_groups[i])
                MoveParameterToGroup(family_doc, filtered_params[i], parse_pg, "temp{}".format(i))
                fam_report.append("ОК. {} изменен".format(filtered_params[i].Definition.Name))

            report.append(fam_report)
            trans.Commit()
            trans.Dispose()
        else:
            report.append("Нет таких параметров. Файл {}".format(family_doc.Title))

        optS = SaveAsOptions()
        optS.OverwriteExistingFile = True
        optS.Compact = True
        optS.MaximumBackups = 1
        family_doc.SaveAs(filepath, optS)
        family_doc.Close(False)

    OUT = report
else:
    OUT = "Нет такой директории"
