import clr
from datetime import datetime
clr.AddReference("RevitAPI")
from Autodesk.Revit.DB import RevitLinkType, FilteredElementCollector, \
    WorksetConfiguration, WorksetConfigurationOption, BuiltInParameter
clr.AddReference("RevitServices")
from RevitServices.Persistence import DocumentManager


doc = DocumentManager.Instance.CurrentDBDocument
uiapp = DocumentManager.Instance.CurrentUIApplication
app = uiapp.Application


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


def create_model_path(path):
    from Autodesk.Revit.DB import ModelPathUtils
    return ModelPathUtils.ConvertUserVisiblePathToModelPath(path)


def load_from(ip_old, ip_new):
    rvt_types = FilteredElementCollector(doc).OfClass(RevitLinkType).ToElements()
    result = []
    start = datetime.now()
    for rvt in rvt_types:
        type_name = rvt.get_Parameter(BuiltInParameter.SYMBOL_NAME_PARAM).AsString()
        path = rvt.Load().GetExternalResourceReference().InSessionPath
        if 'RSN' in path:
            new_path = path.replace(ip_old, ip_new)
            w_opt = WorksetConfigurationOption()
            w_opt.CloseAllWorksets
            try:
                rvt.LoadFrom(create_model_path(new_path), WorksetConfiguration(w_opt))
                info = '{} - Done :)'.format(type_name)
            except Exception:
                info = '{} - Undone :()'.format(type_name)
            result.append(info)
    result.append(datetime.now() - start)
    return result


info = load_from(IN[1], IN[2])
synchronize_with_central(doc, load_from.__name__)

OUT = info
