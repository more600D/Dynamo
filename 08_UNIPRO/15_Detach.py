import clr
clr.AddReference("RevitAPI")
clr.AddReference("RevitAPIUI")
clr.AddReference("RevitServices")

from Autodesk.Revit.DB import *
from Autodesk.Revit.Exceptions import InvalidOperationException
from Autodesk.RevitServer.Sdk.Client import *

def detach_from_server(server_url, file_path):
    gateway = RevitServerGateway.GetServerGateway(server_url)
    try:
        gateway.DetachAndPreserveWorksets(file_path)
        return True
    except InvalidOperationException:
        return False

OUT = 0
