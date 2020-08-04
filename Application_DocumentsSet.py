# -*- coding: utf-8 -*-
import clr
clr.AddReference('RevitAPI')
clr.AddReference('RevitServices')
from RevitServices.Persistence import DocumentManager

add

doc = DocumentManager.Instance.CurrentDBDocument
uiapp = DocumentManager.Instance.CurrentUIApplication
app = uiapp.Application

add
docs = []
for i in app.Documents:
    if not i.IsFamilyDocument:
        docs.append(i)lll

OUT = [i.Title for i in docs]
