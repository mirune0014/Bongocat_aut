@echo off
echo [INFO] Activating virtual environment...
call .venv\Scripts\activate.bat

echo [INFO] Building executable with PyInstaller...
pyinstaller --noconsole --onefile --clean --name "Bongocat" --icon assets\bongocat.ico src\app.py

echo [INFO] Done! Output is in the "dist" folder.
pause
