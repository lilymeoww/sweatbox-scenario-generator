# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['App.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('rsc', 'rsc'),
        ('theme.json', '.'),
        ('utils.py', '.'),
        ('interface.py', '.'),
        ('icons8-plane-50.png', '.')
    ],
    hiddenimports=['PIL._tkinter_finder','customtkinter','tkintermapview'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='sweatbox-scenario-generator',
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
)
