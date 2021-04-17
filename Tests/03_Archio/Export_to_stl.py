import clr
clr.AddReference("RevitAPI")
from Autodesk.Revit.DB import STLExportOptions, STLExportResolution, ExportUnit, \
    FilteredElementCollector, View3D, Extrusion, ElementId, Transaction

clr.AddReference("RevitServices")
from RevitServices.Persistence import DocumentManager

from System.Collections.Generic import List


doc = DocumentManager.Instance.CurrentDBDocument
uiapp = DocumentManager.Instance.CurrentUIApplication
app = uiapp.Application


def get_path_file():
    doc = DocumentManager.Instance.CurrentDBDocument
    title = doc.Title
    path = doc.PathName.split(title)
    return path[0]


def get_3dview_by_name(view_name):
    view_col = FilteredElementCollector(doc).OfClass(View3D)
    for view in view_col:
        if view.Name == view_name:
            return view


def export_to_stl(view_name, file_name):
    doc = DocumentManager.Instance.CurrentDBDocument
    view = get_3dview_by_name(view_name)
    extrusions = FilteredElementCollector(doc).OfClass(Extrusion)
    extrusion_list = List[ElementId]()
    for ex in extrusions:
        extrusion_list.Add(ex.Id)
    with Transaction(doc, 'Hide extrusions elements') as t:
        t.Start()
        view.HideElements(extrusion_list)
        t.Commit()
    stl_opt = STLExportOptions(STLExportResolution.Fine)
    stl_opt.TargetUnit = ExportUnit.Millimeter
    stl_opt.ViewId = view.Id
    folder = get_path_file()
    return doc.Export(folder, file_name, stl_opt), folder + file_name


report = export_to_stl(r'{3D}', doc.Title)
OUT = report
