import System
import clr
clr.AddReference("RevitAPI")
from Autodesk.Revit.DB.ExtensibleStorage import SchemaBuilder, AccessLevel, Entity
clr.AddReference("RevitServices")
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager

doc = DocumentManager.Instance.CurrentDBDocument

pi = doc.ProjectInformation
el = UnwrapElement(IN[1])  # noqa

schemaGuid = System.Guid('720080CB-DA99-40DC-9415-E53F280AA1F8')
schema_builder = SchemaBuilder(schemaGuid).SetReadAccessLevel(AccessLevel.Public)

fbName = schema_builder.AddSimpleField('Username', str)
fbAge = schema_builder.AddSimpleField('UserAge', int)

sch = schema_builder.SetSchemaName('ShvydkoSS').Finish()

fieldName = sch.GetField('Username')
fieldAge = sch.GetField('UserAge')

ent = Entity(sch)

ent.Set(fieldName, 'Сергей Швыдко')
ent.Set(fieldAge, 35)

TransactionManager.Instance.EnsureInTransaction(doc)

el.SetEntity(ent)

TransactionManager.Instance.TransactionTaskDone()

OUT = el
