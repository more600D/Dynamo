import os
import clr
clr.AddReference("RevitAPI")
clr.AddReference("RevitServices")
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager


class Probim:
    def __init__(self):
        self.__doc__ = DocumentManager.Instance.CurrentDBDocument
        self.__uiapp__ = DocumentManager.Instance.CurrentUIApplication
        self.__app__ = self.__uiapp__.Application

    # PROJECT DOCUMENT ______________________________________________________________________________________
    def open_project_document(self, directory, file_name):
        from Autodesk.Revit.DB import OpenOptions, ModelPathUtils
        path_to_file = ModelPathUtils.ConvertUserVisiblePathToModelPath(os.path.join(directory, file_name))
        document = self.__app__.OpenDocumentFile(path_to_file, OpenOptions())
        return document

    def close_document(self, document, issave=False):
        document.Close(issave)

    def synchronize_with_central(self, document, comment):
        from Autodesk.Revit.DB import TransactWithCentralOptions, SynchronizeWithCentralOptions, RelinquishOptions
        r_opt = RelinquishOptions(True)
        r_opt.UserWorksets = True
        r_opt.CheckedOutElements = True
        r_opt.StandardWorksets = True
        synchro_opt = SynchronizeWithCentralOptions()
        synchro_opt.Comment = comment
        synchro_opt.SetRelinquishOptions(r_opt)
        document.SynchronizeWithCentral(TransactWithCentralOptions(), synchro_opt)

    # DOORS _________________________________________________________________________________________________
    def doors_getAll(self, document):
        from Autodesk.Revit.DB import FilteredElementCollector, FamilyInstance, BuiltInCategory
        doors = FilteredElementCollector(document).OfClass(FamilyInstance).OfCategory(BuiltInCategory.OST_Doors)
        return doors.ToElements()

    def doors_isMirrored(self, doors):
        return [door for door in doors if door.Mirrored]


OUT = Probim()
