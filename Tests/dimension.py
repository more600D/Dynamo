import clr
clr.AddReference("RevitAPI")
from Autodesk.Revit.DB import FilteredElementCollector, FamilyInstanceReferenceType, ReferenceArray, Options, XYZ, Solid
clr.AddReference("RevitNodes")
import Revit
clr.ImportExtensions(Revit.Elements)
clr.ImportExtensions(Revit.GeometryConversion)
clr.AddReference("RevitServices")
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager


doc = DocumentManager.Instance.CurrentDBDocument
uiapp = DocumentManager.Instance.CurrentUIApplication
app = uiapp.Application


# def isParallel(v1,v2):
#     return v1.CrossProduct(v2).IsAlmostEqualTo(XYZ(0,0,0))


el = UnwrapElement(IN[1])  # noqa
crv = el.Location.Curve
linedir = crv.GetEndPoint(1) - crv.GetEndPoint(0)

opt = Options()
opt.ComputeReferences = True
opt.IncludeNonVisibleObjects = True
opt.View = doc.ActiveView

gem = el.get_Geometry(opt)

ref = ReferenceArray()

for g in gem:
    if isinstance(g, Solid):
        faces = g.Faces
        for face in faces:
            if face:
                faceNormal = face.FaceNormal
                if faceNormal.CrossProduct(linedir).IsAlmostEqualTo(XYZ(0, 0, 0)):
                    ref.Append(face.Reference)


TransactionManager.Instance.EnsureInTransaction(doc)

dim = doc.Create.NewDimension(doc.ActiveView, crv, ref)

TransactionManager.Instance.TransactionTaskDone()


OUT = crv
