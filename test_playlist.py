import yt_dlp
import sys
import os

# Detectar se está executando como executável PyInstaller
if getattr(sys, 'frozen', False):
    # Executando como executável
    application_path = sys._MEIPASS
    bin_path = os.path.join(application_path, 'bin')
else:
    # Executando como script Python
    application_path = os.path.dirname(os.path.abspath(__file__))
    bin_path = os.path.join(application_path, 'bin')

# Adicionar pasta bin ao PATH se ela existir
if os.path.exists(bin_path):
    os.environ["PATH"] = bin_path + os.pathsep + os.environ["PATH"]
    print(f"FFmpeg path adicionado: {bin_path}")
else:
    print(f"Aviso: Pasta bin não encontrada em {bin_path}")

def test_playlist_url(url):
    print(f"Testando URL: {url}")
    
    try:
        opcoes = {
            'quiet': False,
            'no_warnings': False,
            'extract_flat': True
        }
        
        with yt_dlp.YoutubeDL(opcoes) as ydl:
            print("Extraindo informações...")
            info = ydl.extract_info(url, download=False)
            
            if 'entries' in info:
                print(f"✅ Playlist detectada com {len(info['entries'])} itens:")
                for i, entry in enumerate(info['entries'][:5]):  # Mostrar apenas os primeiros 5
                    if entry:
                        title = entry.get('title', f'Item {i+1}')
                        print(f"  {i+1}. {title}")
                if len(info['entries']) > 5:
                    print(f"  ... e mais {len(info['entries']) - 5} itens")
            else:
                print("✅ Vídeo único detectado:")
                title = info.get('title', 'Sem título')
                print(f"  Título: {title}")
                
    except Exception as e:
        print(f"❌ Erro ao processar URL: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    # URLs de teste
    test_urls = [
        "https://www.youtube.com/playlist?list=PLrAXtmRdnEQy6nuLMHjMZOz59Oq8B9yQH",  # Playlist pequena
        "https://www.youtube.com/watch?v=dQw4w9WgXcQ",  # Vídeo único
    ]
    
    print("=== Teste de Funcionalidade de Playlist ===")
    print(f"Python: {sys.version}")
    print(f"yt-dlp versão: {yt_dlp.version.__version__}")
    print(f"Executável: {getattr(sys, 'frozen', False)}")
    print()
    
    for url in test_urls:
        test_playlist_url(url)
        print("-" * 50)
    
    input("Pressione Enter para sair...")