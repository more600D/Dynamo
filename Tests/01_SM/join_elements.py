import clr
import sys
sys.path.append(r"C:\Users\sssh\OneDrive\09_GitHub\Dynamo\Dynamo-1\Tests\01_SM")
clr.AddReference('Win32Api')
from Win32Api import Win32Api

clr.AddReference("System.Windows.Forms")
from System.Windows.Forms import DialogResult
clr.AddReference("RevitAPI")
from Autodesk.Revit.DB import FilteredElementCollector, Wall, Floor, JoinGeometryUtils, Transaction
clr.AddReference('RevitAPIUI')
from Autodesk.Revit.UI.Events import DialogBoxShowingEventArgs
from Autodesk.Revit.UI import RevitCommandId, PostableCommand, TaskDialogResult
# clr.AddReference("RevitServices")
# from RevitServices.Persistence import DocumentManager

# doc = DocumentManager.Instance.CurrentDBDocument
# uiapp = DocumentManager.Instance.CurrentUIApplication
# app = uiapp.Application


def UiAppOnDialogBoxShowing(sender_uiapp, args):
    if args.GetType().Name == 'DialogBoxShowingEventArgs':
        if args.DialogId == 'Dialog_Revit_DocWarnDialog':
            Win32Api.ClickOk()
            # args.OverrideResult(TaskDialogResult.Ok)
        # else:
        #     args.OverrideResult(1)


walls_col = FilteredElementCollector(doc).OfClass(Wall)
floor_col = FilteredElementCollector(doc).OfClass(Floor)

uiapp.DialogBoxShowing += UiAppOnDialogBoxShowing
with Transaction(doc, 'Join') as t:
    t.Start()
    for f in floor_col:
        for w in walls_col:
            if not JoinGeometryUtils.AreElementsJoined(doc, f, w):
                JoinGeometryUtils.JoinGeometry(doc, f, w)
    t.Commit()
uiapp.DialogBoxShowing -= UiAppOnDialogBoxShowing

# OUT = walls_col, floor_col