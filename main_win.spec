# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['main_win.py'],
             pathex=['D:\\Jace\\Github\\AniPy'],
             binaries=[],
             datas=[('main_win.ui', 'files')],
             hiddenimports=['func.main', 'func.anilist_request', 'func.anilist_getAnime', 'func.anilist_getManga', 'func.trim_list'],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='main_win',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=True )
