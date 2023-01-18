import clr
clr.AddReference("RevitAPI")
from Autodesk.Revit.DB import ElementId
clr.AddReference("RevitServices")
from RevitServices.Persistence import DocumentManager

doc = DocumentManager.Instance.CurrentDBDocument


def export_to_nwc(document, folder_to_export, viewId):
    from Autodesk.Revit.DB import NavisworksExportOptions, OptionalFunctionalityUtils, NavisworksExportScope
    if OptionalFunctionalityUtils.IsNavisworksExporterAvailable():
        nwc_opt = NavisworksExportOptions()
        nwc_opt.ConvertElementProperties = True
        nwc_opt.ExportRoomGeometry = False
        nwc_opt.ExportScope = NavisworksExportScope.View
        nwc_opt.FindMissingMaterials = False
        nwc_opt.ViewId = viewId
        document.Export(folder_to_export, document.Title, nwc_opt)
        return 'Готово! :)'
    else:
        return 'Нужно установить NWC экспортер'


folder = 'C:\\Users\\s.shvydko\\Desktop\\Test'
view_id = ElementId(94488)
info = export_to_nwc(doc, folder, view_id)

OUT = info
