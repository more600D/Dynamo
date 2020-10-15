import clr
clr.AddReference("RevitServices")
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager

doc = DocumentManager.Instance.CurrentDBDocument

el = UnwrapElement(IN[0])  # Выбираем элемент модели

new_name = 'new name'

TransactionManager.Instance.EnsureInTransaction(doc)

elementId = el.GetTypeId() # Получаем id типа экземпляра
elem_type = doc.GetElement(elementId) # получает сам тип
elem_type.Name = new_name # Переименовываем тип

TransactionManager.Instance.TransactionTaskDone()

OUT = elem_type