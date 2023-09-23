# -*- mode: python ; coding: utf-8 -*-


block_cipher = None

datas = []

a = Analysis(
    ['Calendar.py'],
    pathex=[],
    binaries=[],
    datas=datas,
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

a.datas += [('images\\background.jpg','C:\\my stuff\\A level\\comp science\\calender\\images\\background.jpg','DATA'),
            ('images\\dino logo.png','C:\\my stuff\\A level\\comp science\\calender\\images\\dino logo.png','DATA'),
            ('assets\\1-Charlie Brown.mp3', 'C:\\my stuff\\A level\\comp science\\calender\\assets\\1-Charlie Brown.mp3', 'DATA'), ('assets\\2-Paradise.mp3', 'C:\\my stuff\\A level\\comp science\\calender\\assets\\2-Paradise.mp3', 'DATA'), ('assets\\3-Princess of China.mp3', 'C:\\my stuff\\A level\\comp science\\calender\\assets\\3-Princess of China.mp3', 'DATA'), ('assets\\4-Speed of Sound.mp3', 'C:\\my stuff\\A level\\comp science\\calender\\assets\\4-Speed of Sound.mp3', 'DATA'), ('assets\\5-Talk.mp3', 'C:\\my stuff\\A level\\comp science\\calender\\assets\\5-Talk.mp3', 'DATA'), ('assets\\6-Viva la Vida.mp3', 'C:\\my stuff\\A level\\comp science\\calender\\assets\\6-Viva la Vida.mp3', 'DATA')]

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='Calender',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['dino logo.ico'],
)
