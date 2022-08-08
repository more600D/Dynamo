chcp 1251
CD "C:\Program Files\Autodesk\Revit 2021\RevitServerToolCommand\"
set topath=C:\Users\Bim_20.LAN\Desktop\ttt\
set frompath=002_Ilmensky\002-01_WIP\AR\
set modelsfile=C:\Users\Bim_20.LAN\Desktop\models.txt
for /f %%i in (%modelsfile%) do RevitServerTool L "%frompath%%%i.rvt" -s 10.10.1.25 -d "%topath%%%i.rvt" -o