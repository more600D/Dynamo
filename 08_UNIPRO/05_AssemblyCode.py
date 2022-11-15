import clr
clr.AddReference("RevitAPI")
from Autodesk.Revit.DB import AssemblyCodeTable, FilteredElementCollector, WallType, BuiltInParameter, BuiltInCategory

clr.AddReference("RevitServices")
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager
doc = DocumentManager.Instance.CurrentDBDocument


def is_needed_material(material, name):
    if material:
        if name.lower() in material.Name.lower():
            return True


def get_rooms_by_department(department):
    result = []
    rooms = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Rooms).ToElements()
    for room in rooms:
        dep_param = room.get_Parameter(BuiltInParameter.ROOM_DEPARTMENT)
        dep_value = dep_param.AsString().lower()
        if dep_value:
            if isinstance(department, list):
                for d in department:
                    if d.lower() in dep_value:
                        result.append(room)
            else:
                if department.lower() in dep_value:
                    result.append(room)

    return result


def get_walltype_by_material(name):
    result = []
    wall_types = FilteredElementCollector(doc).OfClass(WallType).ToElements()
    for wtype in wall_types:
        com_str = wtype.GetCompoundStructure()
        if com_str:
            layers = com_str.GetLayers()
            for layer in layers:
                mat = doc.GetElement(layer.MaterialId)
                if is_needed_material(mat, name):
                    result.append(wtype)
    return result


def set_assembly_code(material_name, assembly_code_key):
    TransactionManager.Instance.EnsureInTransaction(doc)
    assembly_code = AssemblyCodeTable.GetAssemblyCodeTable(doc).GetKeyBasedTreeEntries()
    vic1 = assembly_code.FindEntry(assembly_code_key)
    types = get_walltype_by_material(material_name)
    result = []
    for t in types:
        param = t.get_Parameter(BuiltInParameter.UNIFORMAT_CODE)
        if param and vic1:
            param.Set(vic1.Key)
            result.append(t)
        else:
            result.append('incorrect assembly code')
    TransactionManager.Instance.TransactionTaskDone()
    return result


# vic1 = set_assembly_code('Керамическая плитка_фартук', 'КС.ВО.06.01.01')
# vic2 = set_assembly_code('Фасадная атмосферостойкая', 'КС.ВО.06.01.01')

dep = 'Техническ'

OUT = get_rooms_by_department(dep)
