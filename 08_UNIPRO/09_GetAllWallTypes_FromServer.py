# -*- coding: utf-8 -*-
from datetime import datetime
import clr
clr.AddReference("RevitAPI")
clr.AddReference("RevitServices")
from RevitServices.Persistence import DocumentManager


doc = DocumentManager.Instance.CurrentDBDocument
uiapp = DocumentManager.Instance.CurrentUIApplication
app = uiapp.Application


def create_path(server_folder, file_name):
    import os
    from Autodesk.Revit.DB import ModelPathUtils
    return ModelPathUtils.ConvertUserVisiblePathToModelPath(os.path.join(server_folder, file_name) + '.rvt')


def synchronize_with_central(document, name):
    from Autodesk.Revit.DB import TransactWithCentralOptions, SynchronizeWithCentralOptions, RelinquishOptions
    r_opt = RelinquishOptions(True)
    r_opt.UserWorksets = True
    r_opt.CheckedOutElements = True
    r_opt.StandardWorksets = True
    trans_opt = TransactWithCentralOptions()
    synchro_opt = SynchronizeWithCentralOptions()
    synchro_opt.Comment = name
    synchro_opt.SetRelinquishOptions(r_opt)
    document.SynchronizeWithCentral(trans_opt, synchro_opt)


def do_something(document):
    result = []
    from Autodesk.Revit.DB import WallType, FilteredElementCollector, BuiltInParameter
    wall_types = FilteredElementCollector(document).OfClass(WallType).ToElements()
    for w_type in wall_types:
        param_name = w_type.get_Parameter(BuiltInParameter.SYMBOL_NAME_PARAM).AsString()
        if param_name not in result:
            result.append(param_name)
    return result


def open_and_change_document(server_folder, file_name):
    from Autodesk.Revit.DB import OpenOptions
    o_opt = OpenOptions()
    path = create_path(server_folder, file_name)
    time_start = datetime.now()
    document = app.OpenDocumentFile(path, o_opt)

    result = do_something(document)
    time_end = datetime.now() - time_start
    synchronize_with_central(document, 'Time spent - {}'.format(time_end))

    document.Close(False)
    return result


files = IN[1]

info = []
time_start = datetime.now()
for key, value in files.items():
    wtypes_name = open_and_change_document(value, key)
    for wname in wtypes_name:
        if wname not in info:
            info.append(wname)
time_end = datetime.now() - time_start
OUT = time_end, info
