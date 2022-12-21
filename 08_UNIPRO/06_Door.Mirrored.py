import clr
clr.AddReference("RevitAPI")
from Autodesk.Revit.DB import FilteredElementCollector, FamilyInstance, BuiltInCategory

clr.AddReference("RevitServices")
from RevitServices.Persistence import DocumentManager

doc = DocumentManager.Instance.CurrentDBDocument


def get_mirrored_doors(document):
    elem_col = FilteredElementCollector(document).OfClass(FamilyInstance).\
        OfCategory(BuiltInCategory.OST_Doors).ToElements()
    mir_doors = []
    fam_name = []
    for elem in elem_col:
        if elem.Mirrored:
            if 'проем' not in elem.Name.lower():
                family_name = document.GetElement(elem.GetTypeId()).Family.Name
                if 'uni' in family_name.lower():
                    mir_doors.append(elem)
                    fam_name.append(family_name)
    return mir_doors, fam_name


OUT = get_mirrored_doors(doc)
