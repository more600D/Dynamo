import clr
clr.AddReference("RevitAPI")
from Autodesk.Revit.DB import FilteredElementCollector, Dimension
clr.AddReference("RevitServices")
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager


doc = DocumentManager.Instance.CurrentDBDocument


typename = IN[1]  # noqa

elements = FilteredElementCollector(doc).OfClass(Dimension).ToElements()

changed = []
TransactionManager.Instance.EnsureInTransaction(doc)

for el in elements:
    if typename in el.Name:
        changed.append(el)
        segments = el.Segments
        if el.NumberOfSegments != 0:
            el.AreSegmentsEqual = False
            el.AreSegmentsEqual = True
            for segment in segments:
                segment.ValueOverride = "1/{}".format(el.NumberOfSegments)
        else:
            el.ValueOverride = ''

TransactionManager.Instance.TransactionTaskDone()

OUT = changed
