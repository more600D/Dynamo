import clr
clr.AddReference("RevitAPI")
from Autodesk.Revit.DB import FilteredElementCollector, Options, FilledRegion, Line, XYZ, UnitUtils, \
    DisplayUnitType, ReferenceArray
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
    if len(edges) < 2:
        return
    shift = UnitUtils.ConvertToInternalUnits(-10 * view.Scale, DisplayUnitType.DUT_MILLIMETERS) * edgesDirection
    dimensionLine = Line.CreateUnbound(filledRegion.get_BoundingBox(view).Min + shift, dimensionDirection)
    references = ReferenceArray()
    for edge in edges:
        references.Append(edge.Reference)
    document.Create.NewDimension(view, dimensionLine, references)


def IsEdgeDirectionSatisfied(edge, edgeDirection):
    for e in edge:
        edgeCurve = e.AsCurve()
        if edgeCurve is None:
            return False
        return edgeCurve.Direction.CrossProduct(edgeDirection).IsAlmostEqualTo(XYZ.Zero)


def FindFilledRegions(document, viewId):
    collector = FilteredElementCollector(document, viewId)
    return collector.OfClass(FilledRegion)


def FindRegionEdges(filledRegion):
    view = filledRegion.Document.GetElement(filledRegion.OwnerViewId)
    options = Options()
    options.View = view
    options.ComputeReferences = True
    edges = []
    for o in filledRegion.get_Geometry(options):
        edges.append(o.Edges)
    return edges


doc = DocumentManager.Instance.CurrentDBDocument

view = doc.ActiveView
filledRegions = FindFilledRegions(doc, view.Id)

TransactionManager.Instance.EnsureInTransaction(doc)

for filledRegion in filledRegions:
    a = CreateDimensions(filledRegion, -1 * view.RightDirection)
    b = CreateDimensions(filledRegion, view.UpDirection)

TransactionManager.Instance.TransactionTaskDone()

OUT = 'Готово!'
