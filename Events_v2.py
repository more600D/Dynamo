import clr
clr.AddReference("RevitAPI")
from Autodesk.Revit.DB import IUpdater, UpdaterId, ChangePriority, UpdaterRegistry
from Autodesk.Revit.DB.Events import DocumentChangedEventArgs
clr.AddReference('RevitAPIUI')
from Autodesk.Revit.UI import TaskDialog
from Autodesk.Revit.UI.Selection import ObjectType, Selection
from Autodesk.Revit.UI.Events import DialogBoxData

clr.AddReference("RevitServices")
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager
from System import Guid

doc = DocumentManager.Instance.CurrentDBDocument
uiapp = DocumentManager.Instance.CurrentUIApplication
app = uiapp.Application


# class MyRoomUpdater(IUpdater):
#     def __init__(self, addinId):
#         self.updaterID = UpdaterId(addinId, Guid('CBCBF6B2-4C06-42d4-97C1-D1B4EB593EFF'))

#     def GetUpdaterId(self):
#         return self.updaterID
    
#     def GetUpdaterName(self):
#         return 'Двойная высота помещения'
    
#     def GetAdditionalInformation(self):
#         return 'MyRoomUpdater (explanation, details, warnings)'
    
#     def GetChangePriority(self):
#         return ChangePriority.RoomsSpacesZones

#     def Execute(self, updaterData):
#         elems = updaterData.GetModifiedElementIds()
#         return elems


# my_updater = MyRoomUpdater(app.ActiveAddInId)
# test = (my_updater.GetUpdaterId())

# # elem = UnwrapElement(IN[1])  # noqa

aaa = None


def get_deleted_elements(sender, args):
    aaa = args.GetDeletedElementIds()
    return aaa


app.DocumentChanged += get_deleted_elements


OUT = aaa
