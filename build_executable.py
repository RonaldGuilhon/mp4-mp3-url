#!/usr/bin/env python3
"""
Script para criar executável portável do YouTube Downloader
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def run_command(command, description):
    """Executa um comando e mostra o progresso"""
    print(f"\n{description}...")
    print(f"Executando: {command}")
    
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    
    if result.returncode != 0:
        print(f"❌ Erro: {description}")
        print(f"Saída de erro: {result.stderr}")
        return False
    else:
        print(f"✅ {description} concluído com sucesso")
        return True

def main():
    print("🚀 Iniciando processo de build do executável portável...")
    
    # Verificar se o Python está instalado
    try:
        python_version = subprocess.check_output([sys.executable, "--version"], text=True).strip()
        print(f"✅ Python encontrado: {python_version}")
    except:
        print("❌ Python não encontrado!")
        return False
    
    # Instalar dependências
    if not run_command(f"{sys.executable} -m pip install -r requirements.txt", "Instalando dependências"):
        return False
    
    # Criar diretório de build se não existir
    build_dir = Path("build")
    dist_dir = Path("dist")
    
    # Limpar builds anteriores
    if build_dir.exists():
        shutil.rmtree(build_dir)
        print("🧹 Diretório build anterior removido")
    
    if dist_dir.exists():
        shutil.rmtree(dist_dir)
        print("🧹 Diretório dist anterior removido")
    
    # Comando PyInstaller para criar executável portável
    pyinstaller_cmd = [
        sys.executable, "-m", "PyInstaller",
        "--onefile",                    # Criar um único arquivo executável
        "--windowed",                   # Não mostrar console (para GUI)
        "--name=YouTubeDownloader",     # Nome do executável
        "--icon=icon.ico",              # Ícone (se existir)
        "--add-data=bin;bin",           # Incluir pasta bin com ffmpeg
        "--hidden-import=tkinter",      # Importação explícita do tkinter
        "--hidden-import=yt_dlp",       # Importação explícita do yt-dlp
        "--clean",                      # Limpar cache antes do build
        "main.py"
    ]
    
    # Verificar se o ícone existe, se não, remover da lista
    if not Path("icon.ico").exists():
        pyinstaller_cmd = [cmd for cmd in pyinstaller_cmd if not cmd.startswith("--icon")]
        print("⚠️  Ícone não encontrado, continuando sem ícone")
    
    # Executar PyInstaller
    pyinstaller_str = " ".join(pyinstaller_cmd)
    if not run_command(pyinstaller_str, "Criando executável com PyInstaller"):
        return False
    
    # Verificar se o executável foi criado
    exe_path = dist_dir / "YouTubeDownloader.exe"
    if exe_path.exists():
        print(f"\n🎉 Executável criado com sucesso!")
        print(f"📁 Localização: {exe_path.absolute()}")
        print(f"📊 Tamanho: {exe_path.stat().st_size / (1024*1024):.1f} MB")
        
        # Criar pasta de distribuição
        release_dir = Path("release")
        if release_dir.exists():
            shutil.rmtree(release_dir)
        release_dir.mkdir()
        
        # Copiar executável para pasta de release
        shutil.copy2(exe_path, release_dir / "YouTubeDownloader.exe")
        
        # Criar arquivo README para distribuição
        readme_content = """# YouTube Downloader - Executável Portável

## Como usar:
1. Execute o arquivo YouTubeDownloader.exe
2. Cole a URL do YouTube no campo apropriado
3. Escolha o formato (MP4 para vídeo ou MP3 para áudio)
4. Selecione o diretório de destino
5. Clique em "Verificar URL" para ver os itens disponíveis
6. Selecione os itens desejados e clique em "Baixar"

## Características:
- ✅ Totalmente portável (não requer instalação)
- ✅ Suporte a vídeos individuais e playlists
- ✅ Download em MP4 (vídeo) e MP3 (áudio)
- ✅ Interface gráfica intuitiva
- ✅ Inclui FFmpeg integrado

## Requisitos do sistema:
- Windows 7 ou superior
- Conexão com a internet

## Observações:
- O primeiro uso pode ser mais lento devido à inicialização
- Alguns antivírus podem alertar sobre o executável (falso positivo)
- Mantenha o software atualizado para melhor compatibilidade
"""
        
        with open(release_dir / "README.txt", "w", encoding="utf-8") as f:
            f.write(readme_content)
        
        print(f"\n📦 Pasta de distribuição criada: {release_dir.absolute()}")
        print("\n✨ Build concluído! Você pode distribuir a pasta 'release' completa.")
        
        return True
    else:
        print("❌ Erro: Executável não foi criado")
        return False

if __name__ == "__main__":
    success = main()
    if success:
        print("\n🎊 Processo concluído com sucesso!")
        input("\nPressione Enter para sair...")
    else:
        print("\n💥 Processo falhou!")
        input("\nPressione Enter para sair...")
    sys.exit(0 if success else 1)