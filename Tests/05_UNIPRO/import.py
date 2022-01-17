import clr
import inspect
clr.AddReference("RevitAPI")
import Autodesk.Revit.DB as ADSK

classes = [item[0] for item in inspect.getmembers(ADSK)]

if 'ForgeTypeId' in classes:
    from Autodesk.Revit.DB import ForgeTypeId as FT
    OUT = dir(FT)
else:
    OUT = classes

def convert_square(param):
    


# OUT = [item[0] for item in inspect.getmembers(ADSK)]
