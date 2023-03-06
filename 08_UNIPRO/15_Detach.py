import os
import clr
from datetime import datetime
clr.AddReference("RevitAPI")
from Autodesk.Revit.DB import SaveAsOptions, DetachFromCentralOption, OpenOptions, WorksetConfiguration, \
     WorksetConfigurationOption, WorksharingSaveAsOptions
clr.AddReference("RevitServices")
from RevitServices.Persistence import DocumentManager

uiapp = DocumentManager.Instance.CurrentUIApplication
app = uiapp.Application


def create_model_path(server_folder, file_name):
    from Autodesk.Revit.DB import ModelPathUtils
    return ModelPathUtils.ConvertUserVisiblePathToModelPath(os.path.join(server_folder, file_name) + '.rvt')


def save_file_to_another_server(path_from, path_to):
    try:
        o_opt = OpenOptions()
        o_opt.Audit = True
        config = WorksetConfiguration(WorksetConfigurationOption.CloseAllWorksets)
        o_opt.SetOpenWorksetsConfiguration(config)
        o_opt.DetachFromCentralOption = DetachFromCentralOption.DetachAndPreserveWorksets
        document = app.OpenDocumentFile(path_from, o_opt)
        save_opt = SaveAsOptions()
        save_opt.OverwriteExistingFile = True
        work_save_opt = WorksharingSaveAsOptions()
        work_save_opt.SaveAsCentral = True
        save_opt.SetWorksharingOptions(work_save_opt)
        document.SaveAs(path_to_save, save_opt)
        document.Close()
        return 'Done :)'
    except Exception:
        return 'Undone :()'


def create_server_path(ip, path):
    return 'RSN://{}/'.format(ip) + path


ip_from = IN[1]
ip_to = IN[2]
folder = IN[3]
files = IN[4]

result = []
start = datetime.now()
for file_name in files:
    full_path_from = create_server_path(ip_from, folder)
    full_path_to = create_server_path(ip_to, folder)
    path_to_open = create_model_path(full_path_from, file_name)
    path_to_save = create_model_path(full_path_to, file_name)
    result.append(save_file_to_another_server(path_to_open, path_to_save))
result.append(datetime.now() - start)

OUT = result
