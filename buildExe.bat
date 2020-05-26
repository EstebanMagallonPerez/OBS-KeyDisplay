del /f "keyViewer.exe"
pyinstaller keyViewer.py --hidden-import engineio.async_drivers.aiohttp --hidden-import engineio.async_aiohttp --onefile --noconsole --icon=key.ico

xcopy ".\dist\keyViewer.exe" ".\"
rmdir /Q /s ".\dist"
rmdir /Q /s ".\build"
del /f "keyViewer.spec"