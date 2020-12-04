rmdir /Q /S build
rmdir /Q /S dist
pyinstaller "Installer_spec.spec"
pause
