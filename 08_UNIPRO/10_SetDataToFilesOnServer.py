import clr
import os
clr.AddReference("RevitAPI")
clr.AddReference("RevitServices")
from RevitServices.Persistence import DocumentManager
uiapp = DocumentManager.Instance.CurrentUIApplication
app = uiapp.Application


def create_path(server_folder, file_name):
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


def set_data_to_walltype(document, name, data):
    from Autodesk.Revit.DB import WallType, FilteredElementCollector, BuiltInParameter
    wall_types = FilteredElementCollector(document).OfClass(WallType).ToElements()
    wtype_list = []
    for wall_type in wall_types:
        type_name = wall_type.get_Parameter(BuiltInParameter.SYMBOL_NAME_PARAM).AsString()
        wtype_list.append(type_name)
    return wtype_list
        # if name.lower() in type_name.lower():
        #     type_group_param = wall_type.get_Parameter(BuiltInParameter.ALL_MODEL_MODEL)
        #     type_group_param.Set(data)
        #     return "Done! :)"
        # else:
        #     return "There is no such wall type. :("


def open_and_change_document(server_folder, file_name, name, data):
    from Autodesk.Revit.DB import OpenOptions, Transaction
    o_opt = OpenOptions()
    path = create_path(server_folder, file_name)
    document = app.OpenDocumentFile(path, o_opt)
    t = Transaction(document, set_data_to_walltype.__name__)
    t.Start()
    result = set_data_to_walltype(document, name, data)
    t.Commit()
    synchronize_with_central(document, 'in {} set {}'.format(name, data))
    document.Close(False)
    return result


# server_path = 'RSN:\\\\srv-eh\\_PilotProject\\01_WIP'
server_path = IN[1]
files = IN[2]
name = IN[3]
data = IN[4]

info = []
for f in files:
    result = open_and_change_document(server_path, f, name, data)
    info.append(result)

OUT = info
