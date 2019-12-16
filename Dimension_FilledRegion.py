import clr
clr.AddReference("RevitAPI")
from Autodesk.Revit.DB import FilteredElementCollector, Options, FilledRegion, Line, XYZ, View
clr.AddReference("RevitServices")
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager


def CreateDimensions(filledRegion, dimensionDirection):
    document = filledRegion.Document
    view = filledRegion.Document.GetElement(filledRegion.OwnerViewId)
    edgesDirection = dimensionDirection.CrossProduct(view.ViewDirection)
    edges = []
    for x in FindRegionEdges(filledRegion):
        if IsEdgeDirectionSatisfied(x, edgesDirection):
            edges.append(x)


def IsEdgeDirectionSatisfied(edge, edgeDirection):
    edgeCurve = Line(edge.AsCurve())
    if edgeCurve is None:
        return False
    return edgeCurve.Direction.CrossProduct(edgeDirection).IsAlmostEqualTo(XYZ.Zero)


def FindFilledRegions(document, viewId):
    collector = FilteredElementCollector(document, viewId)
    return collector.OfClass(FilledRegion)


def FindRegionEdges(filledRegion):
    view = View(filledRegion.Document.GetElement(filledRegion.OwnerViewId))
    options = Options()
    options.View = view
    options.ComputeReferences = True
    return filledRegion.get_Geometry(options)


doc = DocumentManager.Instance.CurrentDBDocument
uiapp = DocumentManager.Instance.CurrentUIApplication
app = uiapp.Application
uidoc = uiapp.ActiveUIDocument

view = doc.ActiveView
fill = FindFilledRegions(doc, view.Id)
mlist = [i for i in fill]

OUT = FindRegionEdges(mlist[0])
