import clr
clr.AddReference("RevitAPI")
from Autodesk.Revit.DB import GraphicsStyleType, BuiltInCategory, Category
clr.AddReference("RevitServices")
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager

doc = DocumentManager.Instance.CurrentDBDocument


def lineweight(fill, weight=IN[4], graphStyle=GraphicsStyleType.Projection):
    return fill.SetLineWeight(weight, graphStyle)


view = doc.ActiveView
scale = view.Scale

floor_fill = Category.GetCategory(doc, BuiltInCategory.OST_FloorsSurfacePattern)
wall_fill = Category.GetCategory(doc, BuiltInCategory.OST_WallsSurfacePattern)
ceilling_fill = Category.GetCategory(doc, BuiltInCategory.OST_CeilingsSurfacePattern)

TransactionManager.Instance.EnsureInTransaction(doc)

if IN[1]:
    lineweight(floor_fill)
elif IN[2]:
    lineweight(wall_fill)
elif IN[3]:
    lineweight(ceilling_fill)

view.Scale = 1
view.Scale = scale

TransactionManager.Instance.TransactionTaskDone()


OUT = floor_fill.Name
