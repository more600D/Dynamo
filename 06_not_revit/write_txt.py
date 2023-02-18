import os
import clr
from io import open
data = IN[0]
clr.AddReference("RevitServices")
from RevitServices.Persistence import DocumentManager
doc = DocumentManager.Instance.CurrentDBDocument
homedir = os.path.expanduser('~') + r'\\Desktop\\{}_{}.txt'.format(doc.Title, IN[1])
with open(homedir, 'w', newline='') as file:
    for d in data:
        file.write(d + '\n')
    file.close()

OUT = data
