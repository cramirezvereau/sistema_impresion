# -*- mode: python ; coding: utf-8 -*-

import sys
import os

block_cipher = None

# Rutas
project_path = os.path.dirname(os.path.abspath(__name__))

# Icono
def find_icon():
    icon_path = os.path.join(project_path, 'images', 'icono.ico')
    if os.path.exists(icon_path):
        return icon_path
    
    # Buscar cualquier .ico
    images_dir = os.path.join(project_path, 'images')
    if os.path.exists(images_dir):
        for file in os.listdir(images_dir):
            if file.endswith('.ico'):
                return os.path.join(images_dir, file)
    
    # Buscar .png y convertirlo mentalmente
    if os.path.exists(images_dir):
        for file in os.listdir(images_dir):
            if file.endswith('.png'):
                print(f"Nota: Encontré {file} pero necesitaría convertirlo a .ico")
    
    return None

icon = find_icon()

# Archivos de datos
added_files = []

# Agregar imágenes
images_dir = os.path.join(project_path, 'images')
if os.path.exists(images_dir):
    added_files.append((images_dir, 'images'))

# Agregar formatos
formats_dir = os.path.join(project_path, 'formats')
if os.path.exists(formats_dir):
    added_files.append((formats_dir, 'formats'))

# Agregar widgets
widgets_dir = os.path.join(project_path, 'widgets')
if os.path.exists(widgets_dir):
    added_files.append((widgets_dir, 'widgets'))

# Agregar Fichas_PDF
fichas_dir = os.path.join(project_path, 'Fichas_PDF')
if os.path.exists(fichas_dir):
    added_files.append((fichas_dir, 'Fichas_PDF'))

a = Analysis(
    ['main.py'],
    pathex=[project_path],
    binaries=[],
    datas=added_files,
    hiddenimports=[
        'formats.base_format',
        'formats.formato1', 
        'formats.formato2',
        'formats.formato3',
        'widgets.hora_widget',
    ],
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

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='Tickets-HB-Chao',
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
    icon=icon,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='Tickets-HB-Chao'
)