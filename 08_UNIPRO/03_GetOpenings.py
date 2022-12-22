# -*- coding: utf-8 -*-
import clr
clr.AddReference("RevitAPI")
from Autodesk.Revit.DB import FilteredElementCollector, RevitLinkInstance, FamilyInstance, BuiltInCategory, \
    BuiltInParameter, Family, Level
from Autodesk.Revit.DB.Structure import StructuralType
clr.AddReference("RevitServices")
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager


doc = DocumentManager.Instance.CurrentDBDocument

def get_rvtlink(document, name):
    rvtlinks = FilteredElementCollector(document).OfClass(RevitLinkInstance).ToElements()
    for r in rvtlinks:
        if name in r.Name:
            return r.GetLinkDocument(), r.GetTotalTransform()

def get_openings(document):
    family_name = 'UNI_Отверстие.Стена_Прямоугольник'
    familyinstanse = FilteredElementCollector(document).OfClass(FamilyInstance). \
                                                        OfCategory(BuiltInCategory.OST_TelephoneDevices). \
                                                        ToElements()
    result = []
    for fam in familyinstanse:
        if fam.Symbol.Family.Name == family_name:
            result.append(fam)
    return result


def get_family_symbol(document, symbol_name):
    fam_col = FilteredElementCollector(doc).OfClass(Family).ToElements()
    for f in fam_col:
        if f.Name == 'UNI_Отверстие.Стена_Прямоугольник':
            for symbol_id in f.GetFamilySymbolIds():
                symbol = document.GetElement(symbol_id)
                sym_name = symbol.get_Parameter(BuiltInParameter.ALL_MODEL_TYPE_NAME).AsString()
                if sym_name == symbol_name:
                    return symbol


def get_level(document, level_name):
    level_col = FilteredElementCollector(doc).OfClass(Level).ToElements()
    for level in level_col:
        if level.Name == level_name:
            return level


link_doc = get_rvtlink(doc, 'ИОС')[0]
transform = get_rvtlink(doc, 'ИОС')[1]
fams = get_openings(link_doc)


loc_point = transform.OfPoint(fams[2].Location.Point)
symbol_name = fams[2].Symbol.get_Parameter(BuiltInParameter.ALL_MODEL_TYPE_NAME).AsString()
symbol = get_family_symbol(doc, symbol_name)
level_name = link_doc.GetElement(fams[2].LevelId).Name
fam_level = get_level(doc, level_name)
orient = fams[2].HandOrientation

TransactionManager.Instance.EnsureInTransaction(doc)

new_open = doc.Create.NewFamilyInstance(loc_point, symbol, orient, fam_level, StructuralType.NonStructural)

TransactionManager.Instance.TransactionTaskDone()

OUT = new_open