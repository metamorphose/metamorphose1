rmdir /S /Q NSIS\_win_bin
mkdir NSIS\_win_bin

C:\Python25\python.exe -OO py2exe_setup.py py2exe -dNSIS/_win_bin

pause