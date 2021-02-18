import clr
clr.AddReference("RevitAPI")
clr.AddReference('RevitNodes')
from Autodesk.Revit.DB import Options, ReferenceArray, XYZ, Line

clr.AddReference("RevitServices")
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager

import Revit
clr.ImportExtensions(Revit.GeometryConversion)


doc = DocumentManager.Instance.CurrentDBDocument
uiapp = DocumentManager.Instance.CurrentUIApplication
app = uiapp.Application


element = UnwrapElement(IN[1])  # noqa

opt = Options()
opt.ComputeReferences = True
opt.IncludeNonVisibleObjects = True
opt.View = doc.ActiveView

element_type = doc.GetElement(element.GetTypeId())
geo = element_type.get_Geometry(opt)
geometry_instance = [g for g in geo if g.GetType().Name == 'Solid' and g.Volume > 0][0]

new_list = []
edges = geometry_instance.Edges

for e in edges:
    curve = e.AsCurve()
    if curve.GetType().Name == 'Line':
        direction = curve.Direction
        if direction.X > 0:
            new_list.append(e.AsCurve().ToProtoType())

refArray = ReferenceArray()


# ref = [l.Reference for l in geometry_instance.SymbolGeometry if l.GetType().Name == 'Line']

# for r in new_list:
#     refArray.Append(r)

# refArray.Append(new_list[0])
# refArray.Append(new_list[1])
# refArray.Append(ref[4])

# TransactionManager.Instance.EnsureInTransaction(doc)
# bnews = []

# pt1 = XYZ(-2.89579276782608E-19, 6.22647337376248E-15, 0)
# pt2 = XYZ(-2.01413037506538E-15, -1.24671916017717, 0)

# line = UnwrapElement(IN[2])  # noqa

# try:
#     dim = doc.Create.NewDimension(doc.ActiveView, line.GeometryCurve, refArray)
# except Exception as error:
#     bnews.append(error)

# TransactionManager.Instance.TransactionTaskDone()


OUT = new_list
