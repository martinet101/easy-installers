# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['Installer.py'],
             pathex=['.'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)

a.datas += [ ('calc.png', '.\\calc.png', 'DATA')]
a.datas += [ ('calc.ico', '.\\calc.ico', 'DATA')]
a.datas += [ ('zip.png', '.\\zip.png', 'DATA')]
a.datas += [ ('zip.ico', '.\\zip.ico', 'DATA')]
a.datas += [ ('music.png', '.\\music.png', 'DATA')]
a.datas += [ ('music.ico', '.\\music.ico', 'DATA')]

pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='Installer',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False , uac_admin=True, icon=input("\n\n\n\nInsert app codename (calc/zip/music): ")+'.ico')
