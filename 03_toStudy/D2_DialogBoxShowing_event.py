import clr
import sys
sys.path.append("D:/code/py_libs")

clr.AddReference('Win32Api')
from Win32Api import Win32Api

import System
from System import Guid, DateTime, Type, Text, IO
from System.IO import StreamReader, File, Directory, FileStream

clr.AddReference('RevitAPI')
import Autodesk
from Autodesk.Revit.DB import *
clr.AddReference('RevitAPIUI')
from Autodesk.Revit.UI import *
from Autodesk.Revit.UI.Events import *
from Autodesk.Revit.DB.Events import *

clr.AddReference("RevitNodes")
clr.AddReference("RevitServices")

import RevitServices
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager

doc = DocumentManager.Instance.CurrentDBDocument
ui_app = DocumentManager.Instance.CurrentUIApplication
app = ui_app.Application
uidoc = DocumentManager.Instance.CurrentUIApplication.ActiveUIDocument

path_to_folder_file = 'C:/RS_logs/'
log_file_name = 'TaskDialogs_info.log'
path_to_log_file = "{}{}".format(path_to_folder_file, log_file_name)
test = []

if not Directory.Exists(path_to_folder_file):
	Directory.CreateDirectory(path_to_folder_file)


def LogSave(info):
	if info:
		string_list_info = []
		string_list_info.append("")
		string_list_info.append(DateTime.Now.ToLocalTime().ToString())
		# string_list_info.append(python_file_name)
		string_list_info.extend(info)
		IO.File.AppendAllLines(path_to_log_file, string_list_info, Text.Encoding.Unicode)


def UiAppOnDialogBoxShowing(sender_uiapp, args):
	activ_doc = sender_uiapp.ActiveUIDocument.Document
	activ_doc_name = "none"
	if activ_doc is not None:
		activ_doc_name = activ_doc.Title
	LogSave(["UiAppOnDialogBoxShowing:", "activ_doc.Title: {}".format(activ_doc_name), "args Type: {}".format(args.GetType().ToString()), "args.DialogId: {}".format(args.DialogId)])
	if args.GetType() == TaskDialogShowingEventArgs:
		if (args.DialogId == "TaskDialog_File_Name_In_Use"):
			args.OverrideResult(1001)
		elif(args.DialogId == "TaskDialog_Unresolved_References"):
			args.OverrideResult(1002)
		elif(args.DialogId == "TaskDialog_Changes_Not_Saved"):
			args.OverrideResult(1001)
		elif(args.DialogId == "TaskDialog_Missing_Third_Party_Updaters"):
			args.OverrideResult(1001)
		else:
			args.OverrideResult(1001)
	elif args.GetType() == DialogBoxShowingEventArgs:
		if args.DialogId == "Dialog_Revit_PartitionsSaveToMaster":
			args.OverrideResult(1)
		if args.DialogId == "Dialog_Revit_DocWarnDialog":
			LogSave(["Win32Api.ClickOk()"])
			Win32Api.ClickOk()
		else:
			args.OverrideResult(1)
	else:
		LogSave(["UiAppOnDialogBoxShowing else args.OverrideResult(1)"])
		args.OverrideResult(1)


def dialog(sender_uiapp, args):
	td = TaskDialog("любое событие")
	td.MainInstruction = "ещё какойто текст"
	td.Id = "наш собственный ID таск диалога"
	td.Show()

if IN[0]:  # noqa
	ui_app.DialogBoxShowing += UiAppOnDialogBoxShowing
	answer = "вы подписались на событие DialogBoxShowing"
	LogSave([answer])
	OUT = answer
else:
	app.DocumentChanged += dialog
	ui_app.DialogBoxShowing -= UiAppOnDialogBoxShowing  # :(
	answer = "вы отписалисть от событие DialogBoxShowing"
	# ui_app.DialogBoxShowing.Dispose()
	# ui_app.DialogBoxShowing.InPlaceSubtract(UiAppOnDialogBoxShowing)
	LogSave([answer])
	OUT = answer
