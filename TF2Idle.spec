# -*- mode: python -*-
# For use with pyinstaller (http://www.pyinstaller.org/) to compile .exe
# - cd to pyinstaller folder and copy TF2Idle directory into a folder named 'TF2Idle'
# - then run 'python build.py TF2Idle/TF2Idle.spec' to build exe
import os, sys

a = Analysis([os.path.join(HOMEPATH,'support\\_mountzlib.py'), os.path.join(HOMEPATH,'support\\useUnicode.py'), 'tf2idle/tf2idle.py', 'tf2idle/AccountDialog.py', 'tf2idle/config.py', 'tf2idle/groupsdialog.py', 'tf2idle/mainwindow.py', 'tf2idle/settingsdialog.py'],
             pathex=['C:\\Users\\Mohammed\\Desktop\\pyinstaller-1.5-rc1'])
pyz = PYZ(a.pure)

files = os.listdir('TF2Idle/images')
for file in files:
	a.datas += [('images' + os.sep + file, 'TF2Idle/images' + os.sep + file, 'DATA')]

exe = EXE( pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name=os.path.join('dist', 'TF2Idle.exe'),
          debug=False,
          strip=False,
          upx=True,
          console=False,
		  icon='TF2Idle/images/tf2idle.ico')