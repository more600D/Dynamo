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


def set_value_to_wall_or_walltype_parameter(document, wall_type_name, param_name, value):
    from Autodesk.Revit.DB import FilteredElementCollector, Wall, BuiltInParameter
    all_walls = FilteredElementCollector(document).OfClass(Wall).ToElements()
    result = []
    for wall in all_walls:
        type_name = wall.WallType.get_Parameter(BuiltInParameter.SYMBOL_NAME_PARAM).AsString()
        if wall_type_name.lower() in type_name.lower():
            param = wall.LookupParameter(param_name)
            if param:
                result.append('instance - {}'.format(param.Definition.Name))
                param.Set(value)
            else:
                wall_type = wall.WallType
                param = wall_type.LookupParameter(param_name)
                if param:
                    result.append('type - {}'.format(param.Definition.Name))
                    param.Set(value)
                else:
                    result.append("There is no parameter")
    return result


def open_and_change_document(server_folder, file_name, wall_type_name, param_name, data):
    from Autodesk.Revit.DB import OpenOptions, Transaction
    o_opt = OpenOptions()
    path = create_path(server_folder, file_name)
    document = app.OpenDocumentFile(path, o_opt)
    t = Transaction(document, set_value_to_wall_or_walltype_parameter.__name__)
    t.Start()
    result = set_value_to_wall_or_walltype_parameter(document, wall_type_name, param_name, data)
    t.Commit()
    synchronize_with_central(document, 'in {} set {}'.format(param_name, data))
    document.Close(False)
    return result


server_path = IN[1]
files = IN[2]
wall_type_name = IN[3]
param_name = IN[4]
data = IN[5]

info = []
for f in files:
    result = open_and_change_document(server_path, f, wall_type_name, param_name, data)
    info.append(result)

OUT = info
