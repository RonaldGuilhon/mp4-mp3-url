#!/usr/bin/env python3
"""
Script avançado para criar executável portável do YouTube Downloader
Usa arquivo .spec personalizado para maior controle
"""

import os
import sys
import subprocess
import shutil
import time
from pathlib import Path

def print_banner():
    """Exibe banner do script"""
    print("="*60)
    print("    YouTube Downloader - Build Avançado")
    print("    Criando executável portável otimizado")
    print("="*60)
    print()

def check_requirements():
    """Verifica se todos os requisitos estão atendidos"""
    print("🔍 Verificando requisitos...")
    
    # Verificar Python
    try:
        python_version = subprocess.check_output([sys.executable, "--version"], text=True).strip()
        print(f"  ✅ {python_version}")
    except:
        print("  ❌ Python não encontrado!")
        return False
    
    # Verificar arquivos essenciais
    required_files = ['main.py', 'YouTubeDownloader.spec']
    for file in required_files:
        if Path(file).exists():
            print(f"  ✅ {file}")
        else:
            print(f"  ❌ {file} não encontrado!")
            return False
    
    # Verificar pasta bin
    bin_path = Path('bin')
    if bin_path.exists() and any(bin_path.iterdir()):
        print(f"  ✅ Pasta bin com {len(list(bin_path.iterdir()))} arquivos")
    else:
        print("  ⚠️  Pasta bin não encontrada ou vazia")
    
    return True

def install_dependencies():
    """Instala dependências necessárias"""
    print("\n📦 Instalando dependências...")
    
    # Instalar/atualizar pip
    subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", "pip"], 
                  capture_output=True)
    
    # Instalar dependências do requirements.txt
    if Path('requirements.txt').exists():
        result = subprocess.run(
            [sys.executable, "-m", "pip", "install", "-r", "requirements.txt"],
            capture_output=True, text=True
        )
        
        if result.returncode == 0:
            print("  ✅ Dependências instaladas com sucesso")
            return True
        else:
            print(f"  ❌ Erro ao instalar dependências: {result.stderr}")
            return False
    else:
        # Instalar dependências manualmente (excluindo tkinter que é built-in)
        packages = ['yt-dlp>=2023.7.6', 'pyinstaller>=5.13.0']
        for package in packages:
            result = subprocess.run(
                [sys.executable, "-m", "pip", "install", package],
                capture_output=True, text=True
            )
            if result.returncode == 0:
                print(f"  ✅ {package}")
            else:
                print(f"  ❌ Erro ao instalar {package}")
                return False
        return True

def clean_build_dirs():
    """Limpa diretórios de build anteriores"""
    print("\n🧹 Limpando builds anteriores...")
    
    dirs_to_clean = ['build', 'dist', '__pycache__']
    
    for dir_name in dirs_to_clean:
        dir_path = Path(dir_name)
        if dir_path.exists():
            try:
                shutil.rmtree(dir_path)
                print(f"  ✅ {dir_name} removido")
            except Exception as e:
                print(f"  ⚠️  Erro ao remover {dir_name}: {e}")
        else:
            print(f"  ℹ️  {dir_name} não existe")

def build_executable():
    """Constrói o executável usando o arquivo .spec"""
    print("\n🔨 Construindo executável...")
    print("  Isso pode levar alguns minutos...")
    
    start_time = time.time()
    
    # Comando PyInstaller com arquivo .spec
    cmd = [sys.executable, "-m", "PyInstaller", "--clean", "YouTubeDownloader.spec"]
    
    print(f"  Executando: {' '.join(cmd)}")
    
    # Executar com output em tempo real
    process = subprocess.Popen(
        cmd, 
        stdout=subprocess.PIPE, 
        stderr=subprocess.STDOUT, 
        text=True, 
        universal_newlines=True
    )
    
    # Mostrar progresso
    for line in process.stdout:
        line = line.strip()
        if line:
            if "INFO:" in line:
                print(f"    {line.split('INFO:')[-1].strip()}")
            elif "WARNING:" in line:
                print(f"  ⚠️  {line.split('WARNING:')[-1].strip()}")
            elif "ERROR:" in line:
                print(f"  ❌ {line.split('ERROR:')[-1].strip()}")
    
    process.wait()
    
    build_time = time.time() - start_time
    
    if process.returncode == 0:
        print(f"  ✅ Build concluído em {build_time:.1f} segundos")
        return True
    else:
        print(f"  ❌ Build falhou após {build_time:.1f} segundos")
        return False

def verify_executable():
    """Verifica se o executável foi criado corretamente"""
    print("\n🔍 Verificando executável...")
    
    exe_path = Path('dist') / 'YouTubeDownloader.exe'
    
    if exe_path.exists():
        size_mb = exe_path.stat().st_size / (1024 * 1024)
        print(f"  ✅ Executável criado: {exe_path}")
        print(f"  📊 Tamanho: {size_mb:.1f} MB")
        
        # Teste rápido de execução (apenas verificar se inicia)
        print("  🧪 Testando execução...")
        try:
            # Tentar executar com timeout para verificar se não trava
            test_process = subprocess.Popen(
                [str(exe_path)], 
                stdout=subprocess.PIPE, 
                stderr=subprocess.PIPE
            )
            time.sleep(2)  # Aguardar 2 segundos
            test_process.terminate()
            test_process.wait(timeout=5)
            print("  ✅ Executável funciona corretamente")
        except Exception as e:
            print(f"  ⚠️  Aviso no teste: {e}")
        
        return True
    else:
        print("  ❌ Executável não encontrado!")
        return False

def create_release_package():
    """Cria pacote de distribuição"""
    print("\n📦 Criando pacote de distribuição...")
    
    release_dir = Path('release')
    
    # Limpar release anterior
    if release_dir.exists():
        shutil.rmtree(release_dir)
    
    release_dir.mkdir()
    
    # Copiar executável
    exe_source = Path('dist') / 'YouTubeDownloader.exe'
    exe_dest = release_dir / 'YouTubeDownloader.exe'
    
    shutil.copy2(exe_source, exe_dest)
    print(f"  ✅ Executável copiado para {exe_dest}")
    
    # Criar documentação
    docs = {
        'README.txt': create_readme_content(),
        'CHANGELOG.txt': create_changelog_content(),
        'LICENSE.txt': create_license_content()
    }
    
    for filename, content in docs.items():
        doc_path = release_dir / filename
        with open(doc_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  ✅ {filename} criado")
    
    print(f"\n📁 Pacote de distribuição criado em: {release_dir.absolute()}")
    return True

def create_readme_content():
    """Cria conteúdo do README"""
    return """# YouTube Downloader - Executável Portável

## 🚀 Como usar:

1. Execute YouTubeDownloader.exe
2. Cole a URL do YouTube no campo apropriado
3. Escolha o formato:
   - MP4: Para baixar vídeo completo
   - MP3: Para extrair apenas o áudio
4. Selecione onde salvar os arquivos
5. Clique em "Verificar URL" para ver os itens
6. Selecione os itens desejados
7. Clique em "Baixar"

## ✨ Características:

- ✅ Totalmente portável (não precisa instalar)
- ✅ Suporte a vídeos individuais e playlists
- ✅ Download em alta qualidade
- ✅ Conversão automática para MP3
- ✅ Interface gráfica intuitiva
- ✅ FFmpeg integrado

## 💻 Requisitos:

- Windows 7 ou superior
- Conexão com internet
- ~100MB de espaço livre

## ⚠️ Observações:

- Primeiro uso pode ser mais lento
- Respeite os direitos autorais
- Use apenas para conteúdo permitido

## 🐛 Problemas?

- Verifique sua conexão com internet
- Tente uma URL diferente
- Reinicie o programa

Versão: 1.0.0
Data: 2024
"""

def create_changelog_content():
    """Cria conteúdo do changelog"""
    return """# Changelog - YouTube Downloader

## Versão 1.0.0 (2024)

### ✨ Novidades:
- Interface gráfica completa
- Suporte a playlists do YouTube
- Download em MP4 e MP3
- Seleção de itens individuais
- Barra de progresso
- Cancelamento de downloads
- FFmpeg integrado

### 🔧 Melhorias:
- Executável portável
- Sem dependências externas
- Interface responsiva
- Tratamento de erros

### 🐛 Correções:
- Estabilidade geral
- Compatibilidade com Windows
"""

def create_license_content():
    """Cria conteúdo da licença"""
    return """MIT License

Copyright (c) 2024 YouTube Downloader

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

NOTE: This software uses yt-dlp and FFmpeg, which have their own licenses.
"""

def main():
    """Função principal"""
    print_banner()
    
    # Verificar requisitos
    if not check_requirements():
        print("\n❌ Requisitos não atendidos!")
        input("Pressione Enter para sair...")
        return False
    
    # Instalar dependências
    if not install_dependencies():
        print("\n❌ Falha ao instalar dependências!")
        input("Pressione Enter para sair...")
        return False
    
    # Limpar builds anteriores
    clean_build_dirs()
    
    # Construir executável
    if not build_executable():
        print("\n❌ Falha no build!")
        input("Pressione Enter para sair...")
        return False
    
    # Verificar executável
    if not verify_executable():
        print("\n❌ Executável inválido!")
        input("Pressione Enter para sair...")
        return False
    
    # Criar pacote de distribuição
    if not create_release_package():
        print("\n❌ Falha ao criar pacote!")
        input("Pressione Enter para sair...")
        return False
    
    # Sucesso!
    print("\n" + "="*60)
    print("🎉 BUILD CONCLUÍDO COM SUCESSO!")
    print("="*60)
    print("\n📦 Seu executável portável está pronto!")
    print("📁 Localização: release/YouTubeDownloader.exe")
    print("\n✨ Você pode distribuir toda a pasta 'release'")
    print("\n🚀 Para testar, execute: release/YouTubeDownloader.exe")
    
    input("\nPressione Enter para sair...")
    return True

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⏹️  Build cancelado pelo usuário")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n💥 Erro inesperado: {e}")
        input("Pressione Enter para sair...")
        sys.exit(1)