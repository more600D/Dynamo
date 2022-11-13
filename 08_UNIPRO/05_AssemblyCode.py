import clr
clr.AddReference("RevitAPI")
from Autodesk.Revit.DB import AssemblyCodeTable

clr.AddReference("RevitServices")
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager


doc = DocumentManager.Instance.CurrentDBDocument

assembly_code = AssemblyCodeTable.GetAssemblyCodeTable(doc).GetKeyBasedTreeEntries()
vic = assembly_code.FindEntry('ВИС').GetChildrenKeys()
OUT = [a.Description for a in assembly_code]
