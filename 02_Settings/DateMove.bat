chcp 1251
set datetime=%date:~6,8%%date:~3,2%%date:~0,2%
CD "C:\Program Files\Autodesk\Revit 2021\RevitServerToolCommand\"
set frompath=003_ZIL2122\003-01_WIP\
::Башня1
set topathB1=S:\ЗИЛ 21-22\КР\Башня 1\
move /y "%topathB1%*.rvt" "S:\ЗИЛ 21-22\КР\Башня 1\!АРХИВ"
set dt=%date:~7,2%-%date:~4,2%-%date:~10
RevitServerTool L "%frompath%ЗИЛ-ГПР-21.22-0591.22_ПП_Башня1_КЖ.rvt" -s 10.10.1.29 -d "%topathB1%%datetime%_ЗИЛ-ГПР-21.22-0591.22_ПП_Башня1_КЖ.rvt" -o
::Башня2
set topathB2=S:\ЗИЛ 21-22\КР\Башня 2\
move /y "%topathB2%*.rvt" "S:\ЗИЛ 21-22\КР\Башня 2\!АРХИВ"
RevitServerTool L "%frompath%ЗИЛ-ГПР-21.22-0591.22_ПП_Башня2_КЖ.rvt" -s 10.10.1.29 -d "%topathB2%%datetime%_ЗИЛ-ГПР-21.22-0591.22_ПП_Башня2_КЖ.rvt" -o
::Башня3
set topathB3=S:\ЗИЛ 21-22\КР\Башня 3\
move /y "%topathB3%*.rvt" "S:\ЗИЛ 21-22\КР\Башня 3\!АРХИВ"
RevitServerTool L "%frompath%ЗИЛ-ГПР-21.22-0591.22_ПП_Башня3_КЖ.rvt" -s 10.10.1.29 -d "%topathB3%%datetime%_ЗИЛ-ГПР-21.22-0591.22_ПП_Башня3_КЖ.rvt" -o
::CO
set frompathCO=003_ZIL2122\003-03_Coordination\
set topathCO=S:\ЗИЛ 21-22\КР\Координационный\
move /y "%topathCO%*.rvt" "S:\ЗИЛ 21-22\КР\Координационный\!АРХИВ"
RevitServerTool L "%frompathCO%ЗИЛ-ГПР-21.22-0591.22_ПП_Оси.rvt" -s 10.10.1.29 -d "%topathCO%%datetime%_ЗИЛ-ГПР-21.22-0591.22_ПП_Оси.rvt" -o
::Общая
set topathFed=S:\ЗИЛ 21-22\КР\Общая модель\
move /y "%topathFed%*.rvt" "S:\ЗИЛ 21-22\КР\Общая модель\!АРХИВ"
RevitServerTool L "%frompath%ЗИЛ-ГПР-21.22-0591.22_ПП_КЖ.rvt" -s 10.10.1.29 -d "%topathFed%%datetime%_ЗИЛ-ГПР-21.22-0591.22_ПП_КЖ.rvt" -o
::Стилобат
set topathST=S:\ЗИЛ 21-22\КР\Стилобат\
move /y "%topathST%*.rvt" "S:\ЗИЛ 21-22\КР\Стилобат\!АРХИВ"
::RevitServerTool L "%frompath%ЗИЛ-ГПР-21.22-0591.22_ПП_Стилобат_КЖ.rvt" -s 10.10.1.29 -d "%topathST%%datetime%_ЗИЛ-ГПР-21.22-0591.22_ПП_Стилобат_КЖ.rvt" -o
RevitServerTool L "%frompath%ЗИЛ-ГПР-21.22-0591.22_ПП_Стилобат_КЖ_2501.rvt" -s 10.10.1.29 -d "%topathST%%datetime%_ЗИЛ-ГПР-21.22-0591.22_ПП_Стилобат_КЖ_2501.rvt" -o