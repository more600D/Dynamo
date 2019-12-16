import clr
clr.AddReference('RevitAPIUI')
from Autodesk.Revit.UI import RevitCommandId, PostableCommand, TaskDialog, TaskDialogCommonButtons, TaskDialogResult
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


def AppDialogShowing(sender, args):
    dialogId = args.DialogId
    promptInfo = "A Revit dialog will be opened.\n"
    promptInfo += "The DialogId of this dialog is " + dialogId + "\n"
    promptInfo += "If you don't want the dialog to open, please press cancel button"

    taskDialog = TaskDialog("Revit")
    taskDialog.Id = "Customer DialogId"
    taskDialog.MainContent = promptInfo
    buttons = TaskDialogCommonButtons.Ok | TaskDialogCommonButtons.Cancel
    taskDialog.CommonButtons = buttons
    result = taskDialog.Show()
    if TaskDialogResult.Cancel == result:
        args.OverrideResult(1)
    else:
        args.OverrideResult(0)


uiapp.DialogBoxShowing += AppDialogShowing
e = uiapp.PostCommand(RevitCommandId.LookupPostableCommandId(PostableCommand.PropertyLine))
uiapp.DialogBoxShowing -= AppDialogShowing

OUT = "Тест"
