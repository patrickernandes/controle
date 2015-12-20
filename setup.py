#setup para gerar executavel no windows com cx_Freeze:
#executar: python setup.py build
#
import sys
from cx_Freeze import setup, Executable
 
buildOptions = dict(packages = [], excludes = [])
 
base = 'Console'
 
executables = [
Executable('controle.py', base=base)]
 
 
setup(name='Controle',
    version = '0.1',
    description = 'Controle Cliente',
    options = dict(build_exe = buildOptions),
    executables = executables)
