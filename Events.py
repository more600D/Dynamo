import clr
clr.AddReference("RevitAPI")
from Autodesk.Revit.DB import FilteredElementCollector
clr.AddReference('RevitAPIUI')
from Autodesk.Revit.UI import UIApplication, RevitCommandId, PostableCommand, TaskDialog
clr.AddReference("RevitServices")
from RevitServices.Persistence import DocumentManager


doc = DocumentManager.Instance.CurrentDBDocument
uiapp = DocumentManager.Instance.CurrentUIApplication
app = uiapp.Application


# def on_dialog_open(sender, event):
#     try:
#         if event.DialogId == 'TaskDialog_Really_Print_Or_Export_Temp_View_Modes':
#             event.OverrideResult(1002)
#             # 1001 call TaskDialogResult.CommandLink1
#             # 1002 call TaskDialogResult.CommandLink2
#             # int(TaskDialogResult.CommandLink2) to check the result
#     except Exception:
#         pass  # print(e) # uncomment this to debug
uiapp = DocumentManager.Instance.CurrentUIApplication
def AppDialogShowing(sender, event):
    return event.DialogId


def my_function(sender, e):
    TaskDialog.Show('Тест', 'Тест1')


uiapp.DialogBoxShowing += my_function
e = uiapp.PostCommand(RevitCommandId.LookupPostableCommandId(PostableCommand.PropertyLine))


OUT = "Тест"
