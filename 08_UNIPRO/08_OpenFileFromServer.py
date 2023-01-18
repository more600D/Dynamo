import os
import clr
clr.AddReference("RevitAPI")
from Autodesk.Revit.DB import BuiltInParameter, Floor, FilteredElementCollector, Transaction
clr.AddReference("RevitServices")
from RevitServices.Persistence import DocumentManager

doc = DocumentManager.Instance.CurrentDBDocument
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


def do_something(document):
    f_type = FilteredElementCollector(document).OfClass(Floor).ToElements()
    param = f_type[0].get_Parameter(BuiltInParameter.ALL_MODEL_INSTANCE_COMMENTS)
    t = Transaction(document, 'test')
    t.Start()
    param.Set('113344')
    t.Commit()
    return 'Done! :)'


def open_and_change_document(server_folder, file_name):
    from Autodesk.Revit.DB import OpenOptions
    from datetime import datetime
    o_opt = OpenOptions()
    path = create_path(server_folder, file_name)
    document = app.OpenDocumentFile(path, o_opt)

    result = do_something(document)
    synchronize_with_central(document, file_name + ' - {}'.format(datetime.now()))

    document.Close(False)
    return result


server_folder = 'RSN:\\\\srv-eh\\_PilotProject\\01_WIP'
file_name = '_ThePilotProject'

result = open_and_change_document(server_folder, file_name)

OUT = result
