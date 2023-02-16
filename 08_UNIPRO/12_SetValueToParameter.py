import clr
clr.AddReference("RevitAPI")
clr.AddReference("RevitServices")
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager


doc = DocumentManager.Instance.CurrentDBDocument



def set_value_to_wall_or_walltype_parameter(document, wall_type_name, param_name, value):
    from Autodesk.Revit.DB import FilteredElementCollector, Wall, BuiltInParameter
    TransactionManager.Instance.EnsureInTransaction(doc)
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
    TransactionManager.Instance.TransactionTaskDone()
    return result


param_name = IN[0]
value = IN[1]
wall_type_name = IN[2]

OUT = set_value_to_wall_or_walltype_parameter(doc, wall_type_name, param_name, value)
