import clr
clr.AddReference("RevitAPI")
from Autodesk.Revit.DB import ElementId, Options, Reference, ViewDetailLevel, FamilyInstanceReferenceType, XYZ, \
    Line, DetailLine, ElementTransformUtils, ReferenceArray
clr.AddReference("RevitServices")
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager

clr.AddReference("RevitNodes")
import Revit
clr.ImportExtensions(Revit.Elements)
from Revit.Elements import *


doc = DocumentManager.Instance.CurrentDBDocument


def create_dimension(element, point1, point2, reference_names_list, view, direction_to_move=XYZ(0, 0, 0)):
    line = Line.CreateBound(point1, point2)
    refArray = ReferenceArray()
    for ref in reference_names_list:
        refArray.Append(element.GetReferenceByName(ref))
    dim = doc.Create.NewDimension(view, line, refArray)
    ElementTransformUtils.MoveElement(doc, dim.Id, direction_to_move)
    return dim


def dim_part(element, orientation, view, offset=0.2, document=doc):
    bb = element.get_BoundingBox(view)
    view_direction = view.ViewDirection.ToString()
    back = XYZ(0, 1, 0).ToString()
    front = XYZ(0, -1, 0).ToString()
    left = XYZ(-1, 0, 0).ToString()
    right = XYZ(1, 0, 0).ToString()
    top = XYZ(0, 0, 1).ToString()
    botton = XYZ(0, 0, -1).ToString()
    # Back or Front
    if view_direction == back or view_direction == front:
        if orientation == 'vertical':
            pt1 = XYZ(bb.Max.X, 0, bb.Min.Z)
            pt2 = XYZ(bb.Max.X, 0, bb.Max.Z)
            return create_dimension(element, pt1, pt2, ['3', '4'], view, XYZ(offset, 0, 0))
        elif orientation == 'horizontal':
            pt1 = XYZ(bb.Min.X, 0, bb.Min.Z)
            pt2 = XYZ(bb.Max.X, 0, bb.Min.Z)
            return create_dimension(element, pt1, pt2, ['1', '2'], view, XYZ(0, 0, -offset))
    # Left or Right
    elif view_direction == left or view_direction == right:
        if orientation == 'vertical':
            pt1 = XYZ(0, bb.Min.Y, bb.Max.Z)
            pt2 = XYZ(0, bb.Min.Y, bb.Min.Z)
            return create_dimension(element, pt1, pt2, ['3', '4'], view, XYZ(0, -offset, 0))
        elif orientation == 'horizontal':
            pt1 = XYZ(0, bb.Min.Y, bb.Min.Z)
            pt2 = XYZ(0, bb.Max.Y, bb.Min.Z)
            return create_dimension(element, pt1, pt2, ['5', '6'], view, XYZ(0, 0, -offset))
    # Top or Botton
    elif view_direction == top or view_direction == botton:
        if orientation == 'vertical':
            pt1 = XYZ(bb.Min.X, bb.Min.Y, 0)
            pt2 = XYZ(bb.Min.X, bb.Max.Y, 0)
            return create_dimension(element, pt1, pt2, ['5', '6'], view, XYZ(-offset, 0, 0))
        elif orientation == 'horizontal':
            pt1 = XYZ(bb.Min.X, bb.Min.Y, 0)
            pt2 = XYZ(bb.Max.X, bb.Min.Y, 0)
            return create_dimension(element, pt1, pt2, ['1', '2'], view, XYZ(0, -offset, 0))


element = UnwrapElement(IN[1])  # noqa

view = doc.ActiveView
TransactionManager.Instance.EnsureInTransaction(doc)
dim1 = dim_part(element, 'vertical', view)
dim1 = dim_part(element, 'horizontal', view)
TransactionManager.Instance.TransactionTaskDone()

OUT = dim1
