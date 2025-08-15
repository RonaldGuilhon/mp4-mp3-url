import yt_dlp
import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
from pathlib import Path

os.environ["PATH"] += os.pathsep + os.path.abspath("bin")

class YouTubeDownloaderGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("YouTube Downloader")
        self.root.geometry("800x600")
        self.root.resizable(True, True)
        
        # Variáveis
        self.url_var = tk.StringVar()
        self.formato_var = tk.StringVar(value="mp4")
        self.diretorio_var = tk.StringVar(value=str(Path.home() / "Downloads"))
        self.playlist_items = []
        self.download_thread = None
        self.cancel_download = False
        
        self.criar_interface()
        
    def criar_interface(self):
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configurar grid
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # URL Input
        ttk.Label(main_frame, text="URL do YouTube:").grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        url_entry = ttk.Entry(main_frame, textvariable=self.url_var, width=60)
        url_entry.grid(row=0, column=1, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 5))
        
        # Formato
        ttk.Label(main_frame, text="Formato:").grid(row=1, column=0, sticky=tk.W, pady=(0, 5))
        formato_frame = ttk.Frame(main_frame)
        formato_frame.grid(row=1, column=1, sticky=tk.W, pady=(0, 5))
        
        ttk.Radiobutton(formato_frame, text="MP4 (Vídeo)", variable=self.formato_var, value="mp4").pack(side=tk.LEFT, padx=(0, 20))
        ttk.Radiobutton(formato_frame, text="MP3 (Áudio)", variable=self.formato_var, value="mp3").pack(side=tk.LEFT)
        
        # Diretório de destino
        ttk.Label(main_frame, text="Salvar em:").grid(row=2, column=0, sticky=tk.W, pady=(0, 5))
        dir_frame = ttk.Frame(main_frame)
        dir_frame.grid(row=2, column=1, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 5))
        dir_frame.columnconfigure(0, weight=1)
        
        ttk.Entry(dir_frame, textvariable=self.diretorio_var, state="readonly").grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 5))
        ttk.Button(dir_frame, text="Procurar", command=self.escolher_diretorio).grid(row=0, column=1)
        
        # Botão verificar playlist
        ttk.Button(main_frame, text="Verificar URL", command=self.verificar_url).grid(row=3, column=1, pady=10, sticky=tk.W)
        
        # Frame para playlist
        self.playlist_frame = ttk.LabelFrame(main_frame, text="Itens da Playlist", padding="5")
        self.playlist_frame.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(10, 0))
        self.playlist_frame.columnconfigure(0, weight=1)
        
        # Scrollable frame para playlist
        self.canvas = tk.Canvas(self.playlist_frame, height=200)
        self.scrollbar = ttk.Scrollbar(self.playlist_frame, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas)
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        self.canvas.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        self.playlist_frame.rowconfigure(0, weight=1)
        
        # Botões de ação
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=5, column=0, columnspan=3, pady=20)
        
        self.download_btn = ttk.Button(button_frame, text="Baixar", command=self.iniciar_download)
        self.download_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        self.cancel_btn = ttk.Button(button_frame, text="Cancelar", command=self.cancelar_download, state="disabled")
        self.cancel_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Button(button_frame, text="Selecionar Todos", command=self.selecionar_todos).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(button_frame, text="Desmarcar Todos", command=self.desmarcar_todos).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(button_frame, text="Limpar", command=self.limpar_interface).pack(side=tk.LEFT)
        
        # Progress bar
        self.progress = ttk.Progressbar(main_frame, mode='indeterminate')
        self.progress.grid(row=6, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(10, 0))
        
        # Status label
        self.status_label = ttk.Label(main_frame, text="Pronto para download")
        self.status_label.grid(row=7, column=0, columnspan=3, pady=(5, 0))
        
        main_frame.rowconfigure(4, weight=1)
        
    def escolher_diretorio(self):
        diretorio = filedialog.askdirectory(initialdir=self.diretorio_var.get())
        if diretorio:
            self.diretorio_var.set(diretorio)
    
    def verificar_url(self):
        url = self.url_var.get().strip()
        if not url:
            messagebox.showerror("Erro", "Por favor, insira uma URL")
            return
            
        self.status_label.config(text="Verificando URL...")
        self.progress.start()
        
        def verificar():
            try:
                opcoes = {
                    'quiet': True,
                    'no_warnings': True,
                    'extract_flat': True
                }
                
                with yt_dlp.YoutubeDL(opcoes) as ydl:
                    info = ydl.extract_info(url, download=False)
                    
                self.root.after(0, lambda: self.processar_info_url(info))
                
            except Exception as e:
                self.root.after(0, lambda: self.erro_verificacao(str(e)))
        
        threading.Thread(target=verificar, daemon=True).start()
    
    def processar_info_url(self, info):
        self.progress.stop()
        
        # Limpar playlist anterior
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        self.playlist_items.clear()
        
        if 'entries' in info:  # É uma playlist
            self.status_label.config(text=f"Playlist encontrada com {len(info['entries'])} itens")
            
            for i, entry in enumerate(info['entries']):
                if entry:
                    var = tk.BooleanVar(value=True)
                    title = entry.get('title', f'Item {i+1}')
                    duration = entry.get('duration_string', 'N/A')
                    
                    frame = ttk.Frame(self.scrollable_frame)
                    frame.pack(fill=tk.X, padx=5, pady=2)
                    
                    cb = ttk.Checkbutton(frame, variable=var, text=f"{title} ({duration})")
                    cb.pack(anchor=tk.W)
                    
                    self.playlist_items.append({
                        'var': var,
                        'url': entry.get('url', ''),
                        'title': title,
                        'id': entry.get('id', '')
                    })
        else:  # É um vídeo único
            self.status_label.config(text="Vídeo único detectado")
            title = info.get('title', 'Vídeo')
            duration = info.get('duration_string', 'N/A')
            
            var = tk.BooleanVar(value=True)
            frame = ttk.Frame(self.scrollable_frame)
            frame.pack(fill=tk.X, padx=5, pady=2)
            
            cb = ttk.Checkbutton(frame, variable=var, text=f"{title} ({duration})")
            cb.pack(anchor=tk.W)
            
            self.playlist_items.append({
                'var': var,
                'url': self.url_var.get(),
                'title': title,
                'id': info.get('id', '')
            })
    
    def erro_verificacao(self, erro):
        self.progress.stop()
        self.status_label.config(text="Erro ao verificar URL")
        messagebox.showerror("Erro", f"Erro ao processar URL:\n{erro}")
    
    def selecionar_todos(self):
        for item in self.playlist_items:
            item['var'].set(True)
    
    def desmarcar_todos(self):
        for item in self.playlist_items:
            item['var'].set(False)
    
    def iniciar_download(self):
        if not self.playlist_items:
            messagebox.showerror("Erro", "Por favor, verifique a URL primeiro")
            return
            
        itens_selecionados = [item for item in self.playlist_items if item['var'].get()]
        
        if not itens_selecionados:
            messagebox.showerror("Erro", "Por favor, selecione pelo menos um item para download")
            return
        
        self.cancel_download = False
        self.download_btn.config(state="disabled")
        self.cancel_btn.config(state="normal")
        self.progress.start()
        
        def download():
            try:
                total_itens = len(itens_selecionados)
                
                for i, item in enumerate(itens_selecionados):
                    if self.cancel_download:
                        break
                        
                    self.root.after(0, lambda i=i, total=total_itens: 
                                   self.status_label.config(text=f"Baixando {i+1}/{total}: {item['title'][:50]}..."))
                    
                    self.baixar_item(item['url'], self.formato_var.get(), self.diretorio_var.get())
                
                if not self.cancel_download:
                    self.root.after(0, lambda: self.download_concluido(total_itens))
                else:
                    self.root.after(0, lambda: self.download_cancelado())
                    
            except Exception as e:
                self.root.after(0, lambda: self.erro_download(str(e)))
        
        self.download_thread = threading.Thread(target=download, daemon=True)
        self.download_thread.start()
    
    def baixar_item(self, url, formato, diretorio):
        opcoes = {
            'outtmpl': os.path.join(diretorio, '%(title)s.%(ext)s'),
            'quiet': True,
        }
        
        if formato.lower() == 'mp3':
            opcoes.update({
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
            })
        else:
            opcoes.update({'format': 'bestvideo+bestaudio/best'})
        
        with yt_dlp.YoutubeDL(opcoes) as ydl:
            ydl.download([url])
    
    def cancelar_download(self):
        self.cancel_download = True
        self.cancel_btn.config(state="disabled")
        self.status_label.config(text="Cancelando download...")
    
    def download_concluido(self, total):
        self.progress.stop()
        self.progress.config(value=0)  # Reset progress bar
        self.download_btn.config(state="normal")
        self.cancel_btn.config(state="disabled")
        self.status_label.config(text=f"Download concluído! {total} arquivo(s) baixado(s)")
        messagebox.showinfo("Sucesso", f"Download concluído!\n{total} arquivo(s) baixado(s) em:\n{self.diretorio_var.get()}")
    
    def download_cancelado(self):
        self.progress.stop()
        self.progress.config(value=0)  # Reset progress bar
        self.download_btn.config(state="normal")
        self.cancel_btn.config(state="disabled")
        self.status_label.config(text="Download cancelado")
        messagebox.showwarning("Cancelado", "Download foi cancelado pelo usuário")
    
    def erro_download(self, erro):
        self.progress.stop()
        self.progress.config(value=0)  # Reset progress bar
        self.download_btn.config(state="normal")
        self.cancel_btn.config(state="disabled")
        self.status_label.config(text="Erro durante o download")
        messagebox.showerror("Erro", f"Erro durante o download:\n{erro}")
    
    def limpar_interface(self):
        """Limpa a interface e reseta todos os campos"""
        # Limpar URL
        self.url_var.set("")
        
        # Reset formato para MP4
        self.formato_var.set("mp4")
        
        # Limpar playlist
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        self.playlist_items.clear()
        
        # Reset progress bar
        self.progress.stop()
        self.progress.config(value=0)
        
        # Reset status
        self.status_label.config(text="Pronto para download")
        
        # Reset botões
        self.download_btn.config(state="normal")
        self.cancel_btn.config(state="disabled")
        
        # Cancelar download se estiver rodando
        if self.download_thread and self.download_thread.is_alive():
            self.cancel_download = True

if __name__ == "__main__":
    root = tk.Tk()
    app = YouTubeDownloaderGUI(root)
    root.mainloop()
