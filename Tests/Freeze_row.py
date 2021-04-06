import clr
clr.AddReference("RevitServices")
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager

doc = DocumentManager.Instance.CurrentDBDocument
schedule = doc.ActiveView
table_data = schedule.GetTableData()

TransactionManager.Instance.EnsureInTransaction(doc)
table_data.FreezeColumnsAndRows = IN[0]  # noqa
TransactionManager.Instance.TransactionTaskDone()
OUT = table_data
