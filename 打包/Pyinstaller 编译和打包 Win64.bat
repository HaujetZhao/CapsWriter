rmdir /s /q .\dist\CapsWriter

pyinstaller --hidden-import sqlite3  --noconfirm   -i "../src/misc/icon.ico" "../src/__init__.pyw"

::pyinstaller --hidden-import sqlite3 --hidden-import PySide2.QtSql   --noconfirm   -i "../src/misc/icon.ico" "../src/__init__.py"

echo d | xcopy /y /s .\dist\rely .\dist\__init__

ren .\dist\__init__\__init__.exe  "_CapsWriter语音输入工具.exe"

move .\dist\__init__ .\dist\CapsWriter

del /F /Q CapsWriter_Win64.7z

7z a -t7z CapsWriter_Win64.7z .\dist\CapsWriter -mx=9 -ms=200m -mf -mhc -mhcf  -mmt -r

pause