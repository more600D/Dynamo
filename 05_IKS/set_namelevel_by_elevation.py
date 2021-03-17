import sys
sys.path.append(r'C:\Program Files (x86)\IronPython 2.7\Lib')
import csv
import clr
clr.AddReference("RevitAPI")
from Autodesk.Revit.DB import FilteredElementCollector, Level
clr.AddReference("RevitServices")
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager


doc = DocumentManager.Instance.CurrentDBDocument


def get_data_from_csv(path):
    with open(path) as f:
        csv_reader = csv.reader(f, delimiter=',')
        data = {}
        for row in csv_reader:
            if len(row) == 2:
                data[row[0]] = int(row[1])
        return data


def get_elements_from_revit(revitapi_class):
    return FilteredElementCollector(doc).OfClass(revitapi_class).ToElements()


path = r"E:\BimOneTime\01_Объект\03_Филармония\08_Dynamo\levels.csv"
levels = get_elements_from_revit(Level)


OUT = levels
OUT.append(get_data_from_csv(path))
