import os
import clr
clr.AddReference("RevitAPI")
from Autodesk.Revit.DB import WallType, FilteredElementCollector, BuiltInParameter, Transaction

clr.AddReference("RevitServices")
from RevitServices.Persistence import DocumentManager

uiapp = DocumentManager.Instance.CurrentUIApplication
app = uiapp.Application

path_dir = IN[0]
type_name = IN[1]
param_name = IN[2]
value = IN[3]


def get_all_rvt_files(directury_path):
    all_files = os.listdir(directury_path)
    return [file for file in all_files if file.endswith('.rvt')]


def delete_file(directory_path):
    all_files = os.listdir(directory_path)
    for file in all_files:
        if '000' in file and file.endswith('.rvt'):
            try:
                os.remove(os.path.join(directory_path, file))
            except Exception:
                pass


def set_value_to_file(rvt_files, type_name, param_name, value):
    for rvt_file in rvt_files:
        doc = app.OpenDocumentFile(os.path.join(path_dir, rvt_file))
        walltype_list = FilteredElementCollector(doc).OfClass(WallType).ToElements()
        t = Transaction(doc, '{}'.format(rvt_file))
        t.Start()
        for wall_type in walltype_list:
            t_name = wall_type.get_Parameter(BuiltInParameter.SYMBOL_NAME_PARAM).AsString()
            if t_name == type_name:
                param = wall_type.LookupParameter(param_name)
                if param:
                    param.Set(value)
        t.Commit()
        doc.Close(True)


rvt_files = get_all_rvt_files(path_dir)
set_value_to_file(rvt_files, type_name, param_name, value)
delete_file(path_dir)

OUT = rvt_files
