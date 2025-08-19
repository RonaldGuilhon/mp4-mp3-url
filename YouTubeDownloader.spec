# -*- mode: python ; coding: utf-8 -*-
"""
Arquivo de especificação personalizado para PyInstaller
Para usar: pyinstaller YouTubeDownloader.spec
"""

import os
from pathlib import Path

# Configurações do build
block_cipher = None
app_name = 'YouTubeDownloader'
script_path = 'main.py'

# Coletar dados adicionais
added_files = []

# Adicionar pasta bin com FFmpeg
bin_path = Path('bin')
if bin_path.exists():
    for file in bin_path.glob('*'):
        if file.is_file():
            added_files.append((str(file), 'bin'))

# Módulos ocultos necessários
hidden_imports = [
    'tkinter',
    'tkinter.ttk',
    'tkinter.filedialog',
    'tkinter.messagebox',
    'yt_dlp',
    'yt_dlp.extractor',
    'threading',
    'pathlib',
    'os',
]

# Análise do script principal
a = Analysis(
    [script_path],
    pathex=[],
    binaries=[],
    datas=added_files,
    hiddenimports=hidden_imports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        # Excluir módulos desnecessários para reduzir tamanho
        'matplotlib',
        'numpy',
        'scipy',
        'pandas',
        'PIL',
        'cv2',
        'tensorflow',
        'torch',
        'jupyter',
        'IPython',
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

# Remover duplicatas e otimizar
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

# Configuração do executável
exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name=app_name,
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,  # Compressão UPX se disponível
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # Sem console para GUI
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='icon.ico' if Path('icon.ico').exists() else None,
)

# Informações de versão (Windows)
version_info = {
    'version': (1, 0, 0, 0),
    'file_version': (1, 0, 0, 0),
    'product_version': (1, 0, 0, 0),
    'file_description': 'YouTube Downloader - Download de vídeos e áudio',
    'product_name': 'YouTube Downloader',
    'copyright': '© 2024 YouTube Downloader',
    'original_filename': f'{app_name}.exe',
    'internal_name': app_name,
}

# Aplicar informações de versão se no Windows
if os.name == 'nt':
    exe.version = version_info