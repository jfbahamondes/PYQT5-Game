# from cx_Freeze import setup, Executable

# setup( name = "Global warning",
#            version = "0.1" ,
#            description = "A game made by Javier Bahamondes" ,
#            executables = [Executable("FronEnd.py")] , )
# '''  1. Este archivo le he llamado ejecutable.py. Llámale como quieras
#      2. Sustituye en Executable el nombre del archivo py o pyw  por el que quieres convertir a exe.
#      3. Abre la línea de comandos en Windows, sitúate en el directorio donde tengas el archivo ejecutable.py y el archivo a convertir en exe y escribe
#     la siguiente línea de comando:
#                                                              py ejecutable.py build.
#     4.Esto te creará una carpeta build que contiene el ejecutable y todos los archivos necesarios
#     NOTA: Recuerda que debes tener instalado cx_freeze. Lo puedes hacer desde la línea de comandos con:
#                                                                                   pip install cx_Freeze

#     '''
#     

import sys
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {"packages": ["os"], "excludes": ["tkinter"]}

# GUI applications require a different base on Windows (the default is for a
# console application).
base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(  name = "Global Warning",
        version = "0.1",
        description = "An aplication made by Javier Bahamondes",
        options = {"build_exe": build_exe_options},
        executables = [Executable("FronEnd.py", base=base)])