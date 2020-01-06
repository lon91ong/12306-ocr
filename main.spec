# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['.\\main.py'],
             pathex=['E:\\WorkShop\\Git\\12306-captcha\\vven'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=['IPython','pandas','PyQT5',],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='TOBA.Local',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=True )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=['vcruntime140.dll','msvcp140.dll'],
               name='TOBA.Local')
