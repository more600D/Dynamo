import os
import clr
from datetime import datetime
from io import open
data = IN[0]
clr.AddReference("RevitServices")
from RevitServices.Persistence import DocumentManager
doc = DocumentManager.Instance.CurrentDBDocument
date = datetime.now()
homedir = os.path.expanduser('~') + r'\\Desktop\\{}_{}_{}.txt'.format(doc.Title, IN[1], date.strftime("%Y%m%d%I%M%S"))
with open(homedir, 'w', newline='') as file:
    for d in data:
        file.write(d + '\n')
    file.close()

OUT = data
