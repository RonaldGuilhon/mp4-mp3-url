# YouTube Downloader - Interface Gráfica

Uma interface gráfica amigável para baixar vídeos e áudios do YouTube usando yt-dlp.

## Características

- ✅ Interface gráfica moderna e intuitiva
- ✅ Suporte para vídeos únicos e playlists
- ✅ Download em formato MP4 (vídeo) ou MP3 (áudio)
- ✅ Seleção personalizada de diretório de destino
- ✅ Visualização e seleção de itens de playlist
- ✅ Botão de cancelar download
- ✅ Barra de progresso e status em tempo real
- ✅ Botões para selecionar/desmarcar todos os itens

## Como usar

1. **Execute o programa:**
   ```bash
   python main.py
   ```

2. **Cole a URL:** Insira a URL do YouTube no campo "URL do YouTube"

3. **Escolha o formato:** Selecione MP4 para vídeo ou MP3 para áudio apenas

4. **Escolha o diretório:** Clique em "Procurar" para selecionar onde salvar os arquivos

5. **Verifique a URL:** Clique em "Verificar URL" para analisar o conteúdo
   - Para vídeos únicos: será exibido o título e duração
   - Para playlists: será exibida uma lista com todos os vídeos disponíveis

6. **Selecione os itens:** 
   - Use os checkboxes para escolher quais vídeos baixar
   - Use "Selecionar Todos" ou "Desmarcar Todos" para facilitar a seleção

7. **Inicie o download:** Clique em "Baixar" para começar

8. **Cancele se necessário:** Use o botão "Cancelar" para interromper o download

## Requisitos

- Python 3.7+
- yt-dlp
- tkinter (geralmente incluído com Python)
- FFmpeg (incluído na pasta `bin/`)

## Estrutura do projeto

```
mp3_mp4_url/
├── main.py          # Aplicação principal com interface gráfica
├── bin/             # Executáveis do FFmpeg
│   ├── ffmpeg.exe
│   ├── ffplay.exe
│   └── ffprobe.exe
└── README.md        # Este arquivo
```

## Funcionalidades da Interface

### Campo URL
- Aceita URLs de vídeos únicos do YouTube
- Aceita URLs de playlists do YouTube
- Validação automática da URL

### Seleção de Formato
- **MP4**: Baixa vídeo completo com áudio
- **MP3**: Extrai apenas o áudio em formato MP3 (192 kbps)

### Gerenciamento de Playlist
- Lista todos os vídeos da playlist com título e duração
- Permite seleção individual de cada item
- Botões para selecionar/desmarcar todos os itens
- Scroll automático para playlists longas

### Controles de Download
- Barra de progresso visual
- Status em tempo real do download
- Contador de progresso (item atual/total)
- Botão de cancelar funcional

### Tratamento de Erros
- Mensagens de erro claras e informativas
- Validação de entrada do usuário
- Recuperação graceful de erros de rede

## Dicas de Uso

1. **Para playlists grandes:** Use os botões de seleção em massa para facilitar a escolha
2. **Organização:** Escolha um diretório específico para manter os downloads organizados
3. **Qualidade:** O formato MP3 usa qualidade de 192 kbps por padrão
4. **Cancelamento:** O botão cancelar pode levar alguns segundos para interromper o download atual

## Solução de Problemas

- **Erro de URL:** Verifique se a URL é válida e acessível
- **Erro de download:** Verifique sua conexão com a internet
- **Erro de permissão:** Certifique-se de ter permissão de escrita no diretório escolhido
- **FFmpeg não encontrado:** Os executáveis devem estar na pasta `bin/`