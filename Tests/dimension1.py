#thanks for all the help everyone
import clr

# Import RevitAPI
clr.AddReference("RevitAPI")
import Autodesk
from Autodesk.Revit.DB import *
import System

clr.AddReference("ProtoGeometry")
from Autodesk.DesignScript import Geometry as geom

# Import Element wrapper extension methods
clr.AddReference("RevitNodes")
import Revit
from Autodesk.Revit.DB import *

# Import ToProtoType, ToRevitType geometry conversion extension methods
clr.ImportExtensions(Revit.GeometryConversion)

clr.AddReference("RevitAPIUI")
from Autodesk.Revit.UI.Selection import ObjectType

clr.AddReference("ProtoGeometry")
from Autodesk.DesignScript import Geometry as geom

# Import DocumentManager and TransactionManager
clr.AddReference("RevitServices")
import RevitServices
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager

doc = DocumentManager.Instance.CurrentDBDocument
uidoc = DocumentManager.Instance.CurrentUIApplication.ActiveUIDocument


def isParallel(v1, v2):
    #it needs two vectors
    return v1.CrossProduct(v2).IsAlmostEqualTo(XYZ(0, 0, 0))

def isAlmostEqualTo(v1, v2):
    return v1.IsAlmostEqualTo(v2)

def isPerpendicular(v1, v2):
    if v1.DotProduct(v2)== 0:
        return True
    else:
        return False


def tolist(obj1):
	if hasattr(obj1,"__iter__"): return obj1
	else: return [obj1]

def CurveToVector(crv):
	vec = geom.Vector.ByTwoPoints(crv.StartPoint,crv.EndPoint)
	return vec

#set the wall orientation, depending on whether exterior or interior is selected
def wallNormal(wall, extOrint):
    if extOrint:
        wallNormal = wall.Orientation.ToVector()
    else:
        wallNormal = wall.Orientation.Negate().ToVector()
    return wallNormal

#this takes the wall location line, shifts it up the to the view cut plane
#and moves it out to the external edge of the wall
def locToCutCrv(wall, wallNormal, lineEndExtend):
	wallLn = wall.Location.Curve
	wallCrv = wallLn.ToProtoType()
	#take the level height, subtract the height of the wall base
	zOf = doc.ActiveView.GenLevel.Elevation-wallCrv.StartPoint.Z
	#get the cut plane offset of the view
	cPlaneH = doc.ActiveView.GetViewRange().GetOffset(PlanViewPlane.CutPlane) #the CutPlane enumeration is like a property of PBP?
	cPlaneHiMM = UnitUtils.ConvertFromInternalUnits(cPlaneH, DisplayUnitType.DUT_MILLIMETERS)	
	wallCrv = geom.Geometry.Translate(wallCrv, geom.Vector.ByCoordinates(0,0, zOf+cPlaneHiMM))
	wallwidthMM = UnitUtils.ConvertFromInternalUnits(wall.Width, DisplayUnitType.DUT_MILLIMETERS)
	wallCrv = geom.Geometry.Translate(wallCrv, wallNormal, (wallwidthMM/2))	

	#get wall curve info
	wallvec = CurveToVector(wallCrv)
	wallorig = geom.Curve.PointAtParameter(wallCrv,0.5)
	walldir1 = geom.Vector.ByTwoPoints(wallorig, wallCrv.StartPoint)
	walldir2 = geom.Vector.ByTwoPoints(wallorig, wallCrv.EndPoint)

	#move points
	ptMvSt = geom.Geometry.Translate(wallCrv.StartPoint, walldir1, lineEndExtend)
	ptMvEnd = geom.Geometry.Translate(wallCrv.EndPoint, walldir2, lineEndExtend)

	#create new line based on extended points
	#this is not a model line! that requires another method
	lineAtExternalEdgeAtCutPlaneHeight = geom.Line.ByStartPointEndPoint(ptMvSt, ptMvEnd).ToRevitType()
	return lineAtExternalEdgeAtCutPlaneHeight

offDist = IN[1]
extOrInt = IN[2]

#if the wall is exterior we need to extend the intersect line
#beyond the exterior face to pick up the intersecting walls
#if the wall is interior, we don't want to extend as far
if extOrInt:
    intersectLineEndExtend = 500
else:
    intersectLineEndExtend = 0

#User Input
ref = uidoc.Selection.PickObject(ObjectType.Element, 'Select A Wall')
#define Targe Wall
targetWall = doc.GetElement(ref)


#let's go get the walls for finding references
intersectedWalls = []
#start by adding our target wall
intersectedWalls.append(targetWall)
#then get all the other walls in the view and test if they intersect the Target Wall
collectedWalls = FilteredElementCollector(doc, doc.ActiveView.Id).OfClass(Wall).ToElements()
for collectedWall in collectedWalls:
    if targetWall.Location.Curve.Intersect(collectedWall.Location.Curve) == SetComparisonResult.Overlap:
        intersectedWalls.append(collectedWall)

#Target Wall external line for intersect check
exLi = locToCutCrv(targetWall, wallNormal(targetWall, extOrInt), intersectLineEndExtend)

#Curve where the dimension will be located
offCrv = geom.Geometry.Translate(exLi.ToProtoType(), wallNormal(targetWall, extOrInt), (offDist))

#lets get the wall edges we want
#only get edges intersecting target side? no this is misleading... we want any reference hitting our external wall
#the problem is actually that the face itsetlf is registering the intersections we don't want e.g. the wrapping ends
frontFaceIW = []
vertEdges = []

opts = Options()
#without compute references, none of this works
opts.ComputeReferences = True
opts.IncludeNonVisibleObjects = True
opts.View = doc.ActiveView
    
for wallInt in intersectedWalls:
    for obj in wallInt.get_Geometry(opts):
        #walls also contain line geometry    
        if isinstance(obj, Solid): 
            for face in obj.Faces:
                #if face is normal is equal to wall normal it is the external face
                if isAlmostEqualTo(wallInt.Orientation, face.ComputeNormal(UV(0.5,0.5))):
                    frontFaceIW.append(face)
                                   
            for edge in obj.Edges:
                #get edges which intersect
                edgeC = edge.AsCurve()
                edgeCNorm = edgeC.Direction.Normalize()
                #if front face edge and edge intersects line and edge is vertical up or vertical down add to list
                if edgeC.Intersect(exLi) != SetComparisonResult.Disjoint and (edgeCNorm.IsAlmostEqualTo(XYZ(0,0,1)) or edgeCNorm.IsAlmostEqualTo(XYZ(0,0,-1))):                    
                    vertEdges.append(edge)					

#so we use the X+Y values as a unique identifier of location (we're less interested in
#the actual unique reference, there may be 2 in the same place)
#we will use these as filtering and sorting values
#if we wanted to use this on sections we'd want to use z value?
vertEdgesLoc = []
for v in vertEdges:
    vLoc = v.AsCurve().GetEndPoint(0).X + v.AsCurve().GetEndPoint(0).Y
    #getting some revit rounding errors, 7dp should be enough!
    vertEdgesLoc.append(round(vLoc,7))


#trying to remove stray intersect edges from adjoining walls
#to identify them, they are not on an intersecting wall front face
#their faces are not both on the target wall

#so we need all the target wall faces
for obj in targetWall.get_Geometry(opts):
    #walls also contain line geometry    
    if isinstance(obj, Solid): 
        faceTW = obj.Faces

#create a holding list containing everything in vertEdges
strayEdges = []        
for v in vertEdges:
    strayEdges.append(v)

#start removing things from holding list to leave only the stray ones
for faIW in frontFaceIW:
    #if edge face 0&1 are both target wall faces we don't want to remove them
    i = 0
    length = len(strayEdges)
    while (i < length):
        if strayEdges[i].GetFace(0) in faceTW:
            strayEdges.Remove(strayEdges[i])
            length = length - 1
        elif strayEdges[i].GetFace(1) in faceTW:
            strayEdges.Remove(strayEdges[i])
            length = length - 1            
        #if our wall is external.... #if edge face is an intersecting wall's front face, we don't want it                
        elif strayEdges[i].GetFace(0) == faIW and extOrInt == True:
            strayEdges.Remove(strayEdges[i])            
            length = length - 1 
        elif strayEdges[i].GetFace(1) == faIW and extOrInt == True:
            strayEdges.Remove(strayEdges[i])
            length = length - 1 
#            strayEdges.Remove(ed)
        #or if the edge reference is to a non-wall
            continue
        i = i+1

#if the wall is exterior, we want to remove references to internal wall edge
if extOrInt == True:
    i=0
    length = len(vertEdgesLoc)
    strayCLoc2 = []
    while (i < length):
        for stray in strayEdges:
            stLoc = stray.AsCurve().GetEndPoint(0).X + stray.AsCurve().GetEndPoint(0).Y
            #getting eroneous values, Revit accuracy not good enough? round is built in method
            if round(vertEdgesLoc[i],7) == round(stLoc,7):
                vertEdges.Remove(vertEdges[i])
                vertEdgesLoc.Remove(vertEdgesLoc[i])
                length = length - 1    
                continue
        i = i+1

#sort the edges using the combined XY location value
vertEdgesSorted = [x for _,x in sorted(zip(vertEdgesLoc,vertEdges))]
vertEdgesLocSorted = sorted(vertEdgesLoc)

#only add uniquely located references
#this is awkward because we test 1 list, then add to the other list
#we need the Temp list, so we know what should be added to the Sub list
vertEdgeUniLocTemp = []
vertEdgeSub = ReferenceArray()
for eL, e in zip(vertEdgesLocSorted, vertEdgesSorted):
    if eL not in vertEdgeUniLocTemp:
        vertEdgeUniLocTemp.append(eL)
        vertEdgeSub.Append(e.Reference)


#we want to pair up the references to create unique dims for the brick dim checker
#convoluted code, ref arrays seem their own beast!
outRefs = []
#define the overall list length
for i in range(vertEdgeSub.Size-1):
    #create the array here so the list nesting is correct
    vertEdgeAr = ReferenceArray()
    #define the sub list length
    while vertEdgeAr.Size < 2:
        #only get add 2 indices for each sub list
        vertEdgeAr.Append(vertEdgeSub[i])
        vertEdgeAr.Append(vertEdgeSub[i+1])
    outRefs.append(vertEdgeAr)

#OUT = len(strayEdges)
#start transaction
TransactionManager.Instance.EnsureInTransaction(doc)
#create dimensions for each pair of referenes
for ref in outRefs:    
    dim = doc.Create.NewDimension(doc.ActiveView, offCrv.ToRevitType(), ref), outRefs, 
#finish transaction    
TransactionManager.Instance.TransactionTaskDone()