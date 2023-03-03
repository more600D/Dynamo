import clr
import os
clr.AddReference("RevitAPI")
from Autodesk.Revit.DB import Wall, Floor, FamilyInstance, FootPrintRoof, BuiltInCategory
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


def set_data_to_parameter(document, elem, param_name, data):
    param = elem.LookupParameter(param_name)
    result = "Готово :)!"
    if param:
        param.Set(data)
    else:
        elem_type = document.GetElement(elem.GetTypeId())
        elem_type_param = elem_type.LookupParameter(param_name)
        if elem_type_param:
            elem_type_param.Set(data)
        else:
            result = "Нет такого параметра :("
    return result


def set_data_to_element(document, class_type, t_name, param_name, data, category):
    from Autodesk.Revit.DB import FilteredElementCollector, BuiltInParameter
    elemes = FilteredElementCollector(document).OfClass(class_type).OfCategory(category).ToElements()
    result = 'Нет такого типа. :('
    info = []
    for elem in elemes:
        type_name = elem.get_Parameter(BuiltInParameter.ELEM_TYPE_PARAM).AsValueString()
        if t_name.lower() in type_name.lower():
            result = set_data_to_parameter(document, elem, param_name, data)
    info.append(result)
    return info


def open_and_change_document(server_folder, file_name, class_type, t_name, param_name,data, category):
    from Autodesk.Revit.DB import OpenOptions, Transaction
    o_opt = OpenOptions()
    path = create_path(server_folder, file_name)
    document = app.OpenDocumentFile(path, o_opt)
    t = Transaction(document, set_data_to_element.__name__)
    t.Start()
    result = set_data_to_element(document, class_type, t_name, param_name, data, category)
    t.Commit()
    synchronize_with_central(document, 'in {}: in {} set {}'.format(t_name, param_name, data))
    document.Close(False)
    return result


server_path = IN[1]
files = IN[2]
type_name = IN[3]
param_name = IN[4]
data = IN[5]
category = IN[6]

info = []
for f in files:
    if category:
        if category == "Стены":
            ost_cat = BuiltInCategory.OST_Walls
            result = open_and_change_document(server_path, f, Wall, type_name, param_name, data, ost_cat)
            info.append(result)
        elif category == "Перекрытия":
            ost_cat = BuiltInCategory.OST_Floors
            result = open_and_change_document(server_path, f, Floor, type_name, param_name, data, ost_cat)
            info.append(result)
        elif category == "Окна":
            ost_cat = BuiltInCategory.OST_Windows
            result = open_and_change_document(server_path, f, FamilyInstance, type_name, param_name, data, ost_cat)
            info.append(result)
        elif category == "Двери":
            ost_cat = BuiltInCategory.OST_Doors
            result = open_and_change_document(server_path, f, FamilyInstance, type_name, param_name, data, ost_cat)
            info.append(result)
        elif category == "Обобщенные модели":
            ost_cat = BuiltInCategory.OST_GenericModel
            result = open_and_change_document(server_path, f, FamilyInstance, type_name, param_name, data, ost_cat)
            info.append(result)
        elif category == "Крыша":
            ost_cat = BuiltInCategory.OST_Roofs
            result = open_and_change_document(server_path, f, FootPrintRoof, type_name, param_name, data, ost_cat)
            info.append(result)
    else:
        info.append("Specify a category!")
        
OUT = info
