import System
import clr
clr.AddReference("RevitAPI")
from Autodesk.Revit.DB.ExtensibleStorage import SchemaBuilder, AccessLevel, Entity
clr.AddReference("RevitServices")
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager

doc = DocumentManager.Instance.CurrentDBDocument

pi = doc.OwnerFamily
# el = UnwrapElement(IN[1])  # noqa

schemaGuid = System.Guid('3cd61681-a611-4a2f-b49c-ea8f0030807b')
schema_builder = SchemaBuilder(schemaGuid).SetReadAccessLevel(AccessLevel.Public)

fbName = schema_builder.AddSimpleField('Author', str)
fbData = schema_builder.AddSimpleField('Data', str)
fbMail = schema_builder.AddSimpleField('Mail', str)

sch = schema_builder.SetSchemaName('ShvydkoSS').Finish()

fieldName = sch.GetField('Author')
fieldData = sch.GetField('Data')
fieldMail = sch.GetField('Mail')

ent = Entity(sch)

ent.Set(fieldName, 'Sergey_Shvydko')
ent.Set(fieldData, '19.12.2019')
ent.Set(fieldMail, 's.s.sh@mail.ru')

TransactionManager.Instance.EnsureInTransaction(doc)

pi.SetEntity(ent)

TransactionManager.Instance.TransactionTaskDone()

OUT = pi
