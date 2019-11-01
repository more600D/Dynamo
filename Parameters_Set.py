import clr
clr.AddReference("RevitServices")
from RevitServices.Persistence import DocumentManager


doc = DocumentManager.Instance.CurrentDBDocument

elements = IN[0]


def set_parameter(items, param_name):
    for i in range(1, len(items)):
        for el in items:
            el.LookupParameter(param_name).Set(i)


set_parameter(elements, 'Марка')

OUT = elements
